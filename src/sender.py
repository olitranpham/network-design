import socket
from socket import AF_INET, SOCK_DGRAM
import argparse
import random
import time

from channel import maybe_flip_bits
from packet import (
    make_data_packet,
    parse_packet,
    MAX_PAYLOAD,
    PKT_ACK,
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
        default=4,
        help="Go-Back-N window size"
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
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--quiet", action="store_true")
    args = ap.parse_args()

    rng = random.Random(args.seed)

    def log(msg: str):
        if not args.quiet:
            print(msg)

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

    retransmissions = 0
    packets_sent = 0
    timeouts = 0

    log(
        f"Sender: file_size={file_size} bytes, "
        f"total_packets={total_packets}, "
        f"window={args.window}, "
        f"timeout={args.timeout}s, "
        f"ack_biterr={args.ack_biterr}, "
        f"ack_loss={args.ack_loss}"
    )

    while base < total_packets:
        while next_seq_num < total_packets and next_seq_num < base + args.window:
            sock.sendto(packet_buffer[next_seq_num], (args.host, args.port))
            packets_sent += 1

            log(
                f"Sent DATA pkt_index={next_seq_num + 1}/{total_packets} "
                f"seq={next_seq_num}"
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
                ack_num = ack["seq"]

                if ack_num < base:
                    log(f"Duplicate/stale ACK{ack_num} received -> ignore")
                else:
                    log(f"Received valid ACK{ack_num}")

                    base = ack_num + 1

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
                log(
                    f"Timeout at base={base} -> retransmit "
                    f"window [{base}, {next_seq_num - 1}]"
                )

                for seq in range(base, next_seq_num):
                    sock.sendto(packet_buffer[seq], (args.host, args.port))
                    packets_sent += 1
                    retransmissions += 1
                    log(f"Retransmitted DATA seq={seq}")

                timer_start = time.time()

    sock.close()
    log(
        f"Sender done. packets_sent={packets_sent}, "
        f"retransmissions={retransmissions}, timeouts={timeouts}"
    )


if __name__ == "__main__":
    main()
