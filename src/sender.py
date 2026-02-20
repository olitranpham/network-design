import socket
from socket import AF_INET, SOCK_DGRAM
import argparse
import random
from channel import maybe_flip_bits

from packet import (
    make_data_packet,
    parse_packet,
    MAX_PAYLOAD,
    PKT_ACK,
)

def toggle(bit: int) -> int:
    return 1 if bit == 0 else 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--host", default="127.0.0.1")
    ap.add_argument("--port", type=int, default=9000)
    ap.add_argument("--file", required=True)
    ap.add_argument("--timeout", type=float, default=0.5, help="ACK wait timeout seconds")
    ap.add_argument("--ack-biterr", type=float, default=0.0)
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

    log(f"Sender: file_size={file_size} bytes, total_packets={total_packets}, timeout={args.timeout}s")

    for pkt_index in range(total_packets):
        start = pkt_index * MAX_PAYLOAD
        end = min(start + MAX_PAYLOAD, file_size)
        chunk = file_data[start:end]

        last_packet = make_data_packet(seq, chunk, total_packets)

        while True:
            sock.sendto(last_packet, (args.host, args.port))
            log(f"Sent DATA pkt_index={pkt_index+1}/{total_packets} seq={seq} bytes={len(chunk)}")

            try:
                raw_ack, _ = sock.recvfrom(2048)
                raw_ack = maybe_flip_bits(raw_ack, args.ack_biterr, rng)
            except socket.timeout:
                retransmissions += 1
                log(f"Timeout waiting for ACK{seq} -> retransmit (total_retx={retransmissions})")
                continue

            try:
                ack = parse_packet(raw_ack)
            except Exception as e:
                retransmissions += 1
                log(f"Failed to parse ACK -> retransmit (err={e}, total_retx={retransmissions})")
                continue

            if not ack["checksum_ok"]:
                retransmissions += 1
                log(f"Corrupt ACK detected -> retransmit (want ACK{seq}, total_retx={retransmissions})")
                continue

            if ack["type"] != PKT_ACK:
                retransmissions += 1
                log(f"Non-ACK packet received -> retransmit (type={ack['type']}, total_retx={retransmissions})")
                continue

            if ack["seq"] != seq:
                retransmissions += 1
                log(f"Wrong ACK: got ACK{ack['seq']}, expected ACK{seq} -> retransmit (total_retx={retransmissions})")
                continue

            log(f"Received valid ACK{ack['seq']} for seq={seq}")
            seq = toggle(seq)
            break

    sock.close()
    log(f"Sender done. retransmissions={retransmissions}")


if __name__ == "__main__":
    main()