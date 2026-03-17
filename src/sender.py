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


def toggle(bit: int) -> int:
    return 1 if bit == 0 else 0


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

    sock = socket.socket(AF_INET, SOCK_DGRAM)
    sock.settimeout(args.timeout)

    seq = 0
    retransmissions = 0
    packets_sent = 0
    timeouts = 0

    log(
        f"Sender: file_size={file_size} bytes, "
        f"total_packets={total_packets}, "
        f"timeout={args.timeout}s, "
        f"ack_biterr={args.ack_biterr}, "
        f"ack_loss={args.ack_loss}"
    )

    for pkt_index in range(total_packets):
        start = pkt_index * MAX_PAYLOAD
        end = min(start + MAX_PAYLOAD, file_size)
        chunk = file_data[start:end]

        last_packet = make_data_packet(seq, chunk, total_packets)

        waiting_for_ack = True
        while waiting_for_ack:
            packets_sent += 1
            sock.sendto(last_packet, (args.host, args.port))
            send_time = time.time()

            log(
                f"Sent DATA pkt_index={pkt_index + 1}/{total_packets} "
                f"seq={seq} bytes={len(chunk)}"
            )

            while True:
                remaining = args.timeout - (time.time() - send_time)
                if remaining <= 0:
                    retransmissions += 1
                    timeouts += 1
                    log(
                        f"Timeout waiting for ACK{seq} -> retransmit "
                        f"(timeouts={timeouts}, total_retx={retransmissions})"
                    )
                    break

                sock.settimeout(remaining)

                try:
                    raw_ack, _ = sock.recvfrom(2048)
                except socket.timeout:
                    retransmissions += 1
                    timeouts += 1
                    log(
                        f"Timeout waiting for ACK{seq} -> retransmit "
                        f"(timeouts={timeouts}, total_retx={retransmissions})"
                    )
                    break

                if maybe_drop_packet(args.ack_loss, rng):
                    log(f"Intentionally dropped received ACK for seq={seq}")
                    continue

                raw_ack = maybe_flip_bits(raw_ack, args.ack_biterr, rng)

                try:
                    ack = parse_packet(raw_ack)
                except Exception as e:
                    log(f"Failed to parse ACK -> ignore until timeout/retry (err={e})")
                    continue

                if not ack["checksum_ok"]:
                    log(f"Corrupt ACK detected for seq={seq} -> ignore until timeout/retry")
                    continue

                if ack["type"] != PKT_ACK:
                    log(
                        f"Non-ACK packet received (type={ack['type']}) "
                        f"-> ignore until timeout/retry"
                    )
                    continue

                if ack["seq"] != seq:
                    log(
                        f"Wrong ACK received: got ACK{ack['seq']}, expected ACK{seq} "
                        f"-> ignore until timeout/retry"
                    )
                    continue

                log(f"Received valid ACK{ack['seq']} for seq={seq}")
                seq = toggle(seq)
                waiting_for_ack = False
                break

    sock.close()
    log(
        f"Sender done. packets_sent={packets_sent}, "
        f"retransmissions={retransmissions}, timeouts={timeouts}"
    )


if __name__ == "__main__":
    main()
