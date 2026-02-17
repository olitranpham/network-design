from socket import *
import argparse

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
    args = ap.parse_args()

    sock = socket(AF_INET, SOCK_DGRAM)
    sock.bind(("", args.port))

    expected_seq = 0
    last_ack_sent = 1  
    received_chunks = []
    total_packets = None

    print(f"Receiver listening on UDP port {args.port}")

    while True:
        data, sender_addr = sock.recvfrom(HEADER_SIZE + MAX_PAYLOAD)

        try:
            pkt = parse_packet(data)
        except Exception:
            sock.sendto(make_ack_packet(last_ack_sent), sender_addr)
            continue

        if pkt["type"] != PKT_DATA:
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

        print(f"Accepted seq={seq} ({len(received_chunks)}/{total_packets})")

        if total_packets is not None and len(received_chunks) >= total_packets:
            break

    with open(args.out, "wb") as f:
        for c in received_chunks:
            f.write(c)

    sock.close()
    print(f"Receiver done. Wrote: {args.out}")


if __name__ == "__main__":
    main()
