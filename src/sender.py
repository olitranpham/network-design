import socket
from socket import AF_INET, SOCK_DGRAM
import argparse
import random
import time
import csv

from channel import maybe_flip_bits
from packet import (
    make_data_packet,
    make_ack_packet,
    make_syn_packet,
    make_fin_packet,
    parse_packet,
    MAX_PAYLOAD,
    PKT_ACK,
    PKT_SYN_ACK,
    PKT_FIN_ACK,
)


def maybe_drop_packet(prob: float, rng: random.Random) -> bool:
    if prob <= 0.0:
        return False
    return rng.random() < prob


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--host", default="127.0.0.1")
    ap.add_argument("--port", type=int, default=9000)
    ap.add_argument("--file", required=True)
    ap.add_argument(
        "--window",
        type=int,
        default=16,
        help="Initial receiver window estimate"
    )
    ap.add_argument(
        "--timeout",
        type=float,
        default=0.5,
        help="ACK wait timeout in seconds"
    )
    ap.add_argument(
        "--ack-biterr",
        type=float,
        default=0.0,
        help="Probability of intentionally corrupting a received ACK packet"
    )
    ap.add_argument(
        "--ack-loss",
        type=float,
        default=0.0,
        help="Probability of intentionally dropping a received ACK packet"
    )
    ap.add_argument("--ssthresh", type=float, default=16.0)
    ap.add_argument("--cwnd-log", default="",
                    help="Optional CSV file for cwnd logging")
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--quiet", action="store_true")
    args = ap.parse_args()

    rng = random.Random(args.seed)

    def log(msg: str):
        if not args.quiet:
            print(msg)

    def record_cwnd(event: str):
        if cwnd_rows is not None:
            cwnd_rows.append({
                "time": time.time() - start_time,
                "event": event,
                "base": base,
                "next_seq_num": next_seq_num,
                "cwnd": round(cwnd, 3),
                "ssthresh": round(ssthresh, 3),
                "rwnd": rwnd,
            })

    with open(args.file, "rb") as f:
        file_data = f.read()

    file_size = len(file_data)
    total_packets = (file_size + MAX_PAYLOAD - 1) // MAX_PAYLOAD

    if total_packets == 0:
        log("Sender: input file is empty, nothing to send")
        return

    packet_buffer = []
    for pkt_index in range(total_packets):
        start = pkt_index * MAX_PAYLOAD
        end = min(start + MAX_PAYLOAD, file_size)
        chunk = file_data[start:end]
        packet_buffer.append(make_data_packet(pkt_index, chunk, total_packets))

    sock = socket.socket(AF_INET, SOCK_DGRAM)
    sock.settimeout(0.05)

    base = 0
    next_seq_num = 0
    timer_start = None

    cwnd = 1.0
    ssthresh = args.ssthresh
    rwnd = args.window
    dup_ack_count = 0
    in_fast_recovery = False

    retransmissions = 0
    packets_sent = 0
    timeouts = 0

    start_time = time.time()
    cwnd_rows = [] if args.cwnd_log else None

    log(
        f"Sender: file_size={file_size} bytes, "
        f"total_packets={total_packets}, "
        f"timeout={args.timeout}s, "
        f"cwnd={cwnd}, "
        f"ssthresh={ssthresh}, "
        f"rwnd={rwnd}, "
        f"ack_biterr={args.ack_biterr}, "
        f"ack_loss={args.ack_loss}"
    )

    # Three-way handshake
    while True:
        sock.sendto(make_syn_packet(), (args.host, args.port))
        log("Sender: sent SYN")

        wait_start = time.time()
        got_syn_ack = False

        while time.time() - wait_start < args.timeout:
            try:
                raw_pkt, _ = sock.recvfrom(2048)
                pkt = parse_packet(raw_pkt)

                if pkt["type"] == PKT_SYN_ACK and pkt["checksum_ok"]:
                    rwnd = pkt["rwnd"]
                    got_syn_ack = True
                    break
            except socket.timeout:
                pass
            except Exception:
                pass

        if got_syn_ack:
            log("Sender: received SYN-ACK")
            sock.sendto(make_ack_packet(0, rwnd), (args.host, args.port))
            log("Sender: sent ACK, connection ESTABLISHED")
            break

        log("Sender: SYN timeout, retransmitting")

    record_cwnd("start")

    while base < total_packets:
        send_window = max(1, min(int(cwnd), rwnd))

        while next_seq_num < total_packets and next_seq_num < base + send_window:
            sock.sendto(packet_buffer[next_seq_num], (args.host, args.port))
            packets_sent += 1

            log(
                f"Sent DATA pkt_index={next_seq_num + 1}/{total_packets} "
                f"seq={next_seq_num}, cwnd={cwnd:.2f}, rwnd={rwnd}, "
                f"send_window={send_window}"
            )

            if base == next_seq_num:
                timer_start = time.time()

            next_seq_num += 1

        try:
            raw_ack, _ = sock.recvfrom(2048)

            if maybe_drop_packet(args.ack_loss, rng):
                log("Intentionally dropped received ACK packet")
                raise socket.timeout

            raw_ack = maybe_flip_bits(raw_ack, args.ack_biterr, rng)

            try:
                ack = parse_packet(raw_ack)
            except Exception as e:
                log(f"Failed to parse ACK -> ignore (err={e})")
                ack = None

            if ack is None:
                pass
            elif not ack["checksum_ok"]:
                log("Corrupt ACK detected -> ignore")
            elif ack["type"] != PKT_ACK:
                log(f"Non-ACK packet received (type={ack['type']}) -> ignore")
            else:
                ack_num = ack["ack"]
                rwnd = ack["rwnd"]

                if ack_num < base:
                    if ack_num == base - 1:
                        dup_ack_count += 1
                        log(f"Duplicate ACK{ack_num} received, count={dup_ack_count}")

                        if dup_ack_count == 3:
                            ssthresh = max(cwnd / 2, 2)
                            cwnd = ssthresh + 3
                            in_fast_recovery = True

                            sock.sendto(packet_buffer[base], (args.host, args.port))
                            packets_sent += 1
                            retransmissions += 1

                            log(
                                f"Triple duplicate ACKs -> fast retransmit seq={base}, "
                                f"cwnd={cwnd:.2f}, ssthresh={ssthresh:.2f}"
                            )
                            record_cwnd("fast_retransmit")

                        elif dup_ack_count > 3 and in_fast_recovery:
                            cwnd += 1
                            record_cwnd("fast_recovery_dup_ack")

                    else:
                        log(f"Stale ACK{ack_num} received -> ignore")

                else:
                    log(f"Received valid ACK{ack_num}")

                    base = ack_num + 1
                    dup_ack_count = 0

                    if in_fast_recovery:
                        cwnd = ssthresh
                        in_fast_recovery = False
                        record_cwnd("fast_recovery_exit")
                    elif cwnd < ssthresh:
                        cwnd += 1
                        record_cwnd("slow_start")
                    else:
                        cwnd += 1 / cwnd
                        record_cwnd("congestion_avoidance")

                    if base == next_seq_num:
                        timer_start = None
                    else:
                        timer_start = time.time()

        except socket.timeout:
            pass

        if timer_start is not None:
            elapsed = time.time() - timer_start
            if elapsed >= args.timeout:
                timeouts += 1
                ssthresh = max(cwnd / 2, 2)
                cwnd = 1.0
                dup_ack_count = 0
                in_fast_recovery = False

                log(
                    f"Timeout at base={base} -> cwnd reset to {cwnd:.2f}, "
                    f"ssthresh={ssthresh:.2f}, retransmit window "
                    f"[{base}, {next_seq_num - 1}]"
                )
                record_cwnd("timeout")

                for seq in range(base, next_seq_num):
                    sock.sendto(packet_buffer[seq], (args.host, args.port))
                    packets_sent += 1
                    retransmissions += 1
                    log(f"Retransmitted DATA seq={seq}")

                timer_start = time.time()

    # Connection teardown
    while True:
        sock.sendto(make_fin_packet(total_packets), (args.host, args.port))
        log("Sender: sent FIN")

        wait_start = time.time()
        got_fin_ack = False

        while time.time() - wait_start < args.timeout:
            try:
                raw_pkt, _ = sock.recvfrom(2048)
                pkt = parse_packet(raw_pkt)

                if pkt["type"] == PKT_FIN_ACK and pkt["checksum_ok"]:
                    got_fin_ack = True
                    break
            except socket.timeout:
                pass
            except Exception:
                pass

        if got_fin_ack:
            sock.sendto(make_ack_packet(total_packets, rwnd), (args.host, args.port))
            log("Sender: received FIN-ACK, sent final ACK, connection CLOSED")
            break

        log("Sender: FIN timeout, retransmitting")

    sock.close()

    if args.cwnd_log:
        with open(args.cwnd_log, "w", newline="") as f:
            writer = csv.DictWriter(
                f,
                fieldnames=["time", "event", "base", "next_seq_num",
                            "cwnd", "ssthresh", "rwnd"]
            )
            writer.writeheader()
            writer.writerows(cwnd_rows)

    log(
        f"Sender done. packets_sent={packets_sent}, "
        f"retransmissions={retransmissions}, timeouts={timeouts}, "
        f"final_cwnd={cwnd:.2f}, ssthresh={ssthresh:.2f}"
    )


if __name__ == "__main__":
    main()
    