from socket import *
import argparse
import random
import time
from channel import maybe_flip_bits

from packet import (
    parse_packet,
    make_ack_packet,
    make_syn_ack_packet,
    make_fin_ack_packet,
    PKT_DATA,
    PKT_ACK,
    PKT_SYN,
    PKT_FIN,
    MAX_PAYLOAD,
    HEADER_SIZE,
)


def maybe_drop_packet(prob: float, rng: random.Random) -> bool:
    if prob <= 0.0:
        return False
    return rng.random() < prob


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--port", type=int, default=9000)
    ap.add_argument("--out", required=True, help="output file path")
    ap.add_argument("--data-biterr", type=float, default=0.0)
    ap.add_argument("--data-loss", type=float, default=0.0)
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--recv-window", type=int, default=16)
    ap.add_argument("--drop-data-seq", type=int, default=-1,
                    help="Drop one DATA packet with this seq number for Reno demo")
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
    last_ack_sent = -1
    received_chunks = []
    total_packets = None
    dropped_demo_packet = False

    log(f"Receiver listening on UDP port {args.port}")

    # Three-way handshake
    sender_addr = None
    while True:
        data, sender_addr = sock.recvfrom(HEADER_SIZE + MAX_PAYLOAD)

        try:
            pkt = parse_packet(data)
        except Exception:
            continue

        if pkt["type"] == PKT_SYN and pkt["checksum_ok"]:
            log("Receiver: received SYN")
            sock.sendto(make_syn_ack_packet(args.recv_window), sender_addr)
            log("Receiver: sent SYN-ACK")
            break

    while True:
        data, sender_addr = sock.recvfrom(HEADER_SIZE + MAX_PAYLOAD)

        try:
            pkt = parse_packet(data)
        except Exception:
            continue

        if pkt["type"] == PKT_ACK and pkt["checksum_ok"]:
            log("Receiver: received ACK, connection ESTABLISHED")
            break

    while True:
        data, sender_addr = sock.recvfrom(HEADER_SIZE + MAX_PAYLOAD)

        if maybe_drop_packet(args.data_loss, rng):
            log("Intentionally dropped received DATA packet")
            continue

        data = maybe_flip_bits(data, args.data_biterr, rng)

        try:
            pkt = parse_packet(data)
        except Exception:
            if last_ack_sent >= 0:
                sock.sendto(make_ack_packet(last_ack_sent, args.recv_window), sender_addr)
            continue

        if pkt["type"] == PKT_FIN and pkt["checksum_ok"]:
            log("Receiver: received FIN")
            sock.sendto(make_fin_ack_packet(last_ack_sent), sender_addr)
            log("Receiver: sent FIN-ACK")
            break

        if pkt["type"] != PKT_DATA:
            if last_ack_sent >= 0:
                sock.sendto(make_ack_packet(last_ack_sent, args.recv_window), sender_addr)
            continue

        if not pkt["checksum_ok"]:
            if last_ack_sent >= 0:
                sock.sendto(make_ack_packet(last_ack_sent, args.recv_window), sender_addr)
            continue

        seq = pkt["seq"]

        if seq == args.drop_data_seq and not dropped_demo_packet:
            dropped_demo_packet = True
            log(f"Demo drop: intentionally dropped DATA seq={seq}")
            continue

        if total_packets is None:
            total_packets = pkt["total_packets"]
            received_chunks = [b""] * total_packets

        if seq != expected_seq:
            if last_ack_sent >= 0:
                sock.sendto(make_ack_packet(last_ack_sent, args.recv_window), sender_addr)
            log(f"Out-of-order DATA seq={seq}, expected={expected_seq} -> resend ACK{last_ack_sent}")
            continue

        received_chunks[seq] = pkt["payload"]

        sock.sendto(make_ack_packet(seq, args.recv_window), sender_addr)
        last_ack_sent = seq
        expected_seq += 1

        log(f"Accepted seq={seq} ({expected_seq}/{total_packets}), rwnd={args.recv_window}")

        if total_packets is not None and expected_seq >= total_packets:
            break

    # Wait for FIN if transfer ended normally
    while True:
        try:
            sock.settimeout(0.2)
            data, sender_addr = sock.recvfrom(HEADER_SIZE + MAX_PAYLOAD)
        except timeout:
            break

        try:
            pkt = parse_packet(data)
        except Exception:
            continue

        if pkt["type"] == PKT_FIN and pkt["checksum_ok"]:
            log("Receiver: received FIN")
            sock.sendto(make_fin_ack_packet(last_ack_sent), sender_addr)
            log("Receiver: sent FIN-ACK")
            break

    if args.linger > 0:
        sock.settimeout(0.1)
        end_time = time.time() + args.linger
        while time.time() < end_time:
            try:
                data, sender_addr = sock.recvfrom(HEADER_SIZE + MAX_PAYLOAD)
            except timeout:
                continue

            try:
                pkt = parse_packet(data)
                if pkt["type"] == PKT_FIN:
                    sock.sendto(make_fin_ack_packet(last_ack_sent), sender_addr)
                elif last_ack_sent >= 0:
                    sock.sendto(make_ack_packet(last_ack_sent, args.recv_window), sender_addr)
            except Exception:
                pass

    with open(args.out, "wb") as f:
        for c in received_chunks:
            f.write(c)

    sock.close()
    log(f"Receiver done. Wrote: {args.out}")


if __name__ == "__main__":
    main()
    