from socket import *
import argparse
import random
import time
from channel import maybe_flip_bits

from packet import (
    parse_packet,
    make_ack_packet,
    PKT_DATA,
    MAX_PAYLOAD,
    HEADER_SIZE,
)

def toggle(bit: int) -> int:
    return 1 if bit == 0 else 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--port", type=int, default=9000)
    ap.add_argument("--out", required=True, help="output file path")
    ap.add_argument("--data-biterr", type=float, default=0.0)
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--linger", type=float, default=1.0,
                    help="Seconds to keep replying with last ACK after file complete")
    ap.add_argument("--quiet", action="store_true")
    args = ap.parse_args()
    rng = random.Random(args.seed)

    def log(msg: str):
        if not args.quiet:
            print(msg)

    sock = socket(AF_INET, SOCK_DGRAM)
    sock.bind(("", args.port))

    expected_seq = 0
    last_ack_sent = 1
    received_chunks = []
    total_packets = None

    log(f"Receiver listening on UDP port {args.port}")

    while True:
        data, sender_addr = sock.recvfrom(HEADER_SIZE + MAX_PAYLOAD)
        data = maybe_flip_bits(data, args.data_biterr, rng)

        try:
            pkt = parse_packet(data)
        except Exception:
            # corrupt, resend last ACK
            sock.sendto(make_ack_packet(last_ack_sent), sender_addr)
            continue

        if pkt["type"] != PKT_DATA:
            # not a DATA packet, resend last ACK
            sock.sendto(make_ack_packet(last_ack_sent), sender_addr)
            continue

        if not pkt["checksum_ok"]:
            sock.sendto(make_ack_packet(last_ack_sent), sender_addr)
            continue

        seq = pkt["seq"]

        if seq != expected_seq:
            sock.sendto(make_ack_packet(last_ack_sent), sender_addr)
            continue

        if total_packets is None:
            total_packets = pkt["total_packets"]

        received_chunks.append(pkt["payload"])

        sock.sendto(make_ack_packet(seq), sender_addr)
        last_ack_sent = seq
        expected_seq = toggle(expected_seq)

        log(f"Accepted seq={seq} ({len(received_chunks)}/{total_packets})")

        if total_packets is not None and len(received_chunks) >= total_packets:
            break

    # linger to help sender receive the final ACK even if gets corrupted
    if args.linger > 0:
        sock.settimeout(0.1)
        end_time = time.time() + args.linger
        while time.time() < end_time:
            try:
                data, sender_addr = sock.recvfrom(HEADER_SIZE + MAX_PAYLOAD)
            except timeout:
                continue

            try:
                sock.sendto(make_ack_packet(last_ack_sent), sender_addr)
            except Exception:
                pass

    with open(args.out, "wb") as f:
        for c in received_chunks:
            f.write(c)

    sock.close()
    log(f"Receiver done. Wrote: {args.out}")


if __name__ == "__main__":
    main()