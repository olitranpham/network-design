import socket
from socket import AF_INET, SOCK_DGRAM
import argparse

from packet import (
    make_data_packet,
    parse_packet,
    MAX_PAYLOAD,
    HEADER_SIZE,
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
    args = ap.parse_args()

    with open(args.file, "rb") as f:
        file_data = f.read()

    file_size = len(file_data)
    total_packets = (file_size + MAX_PAYLOAD - 1) // MAX_PAYLOAD

    sock = socket.socket(AF_INET, SOCK_DGRAM)
    sock.settimeout(args.timeout)

    seq = 0
    retransmissions = 0

    print(f"Sender: file_size={file_size} bytes, total_packets={total_packets}, timeout={args.timeout}s")

    for pkt_index in range(total_packets):
        start = pkt_index * MAX_PAYLOAD
        end = min(start + MAX_PAYLOAD, file_size)
        chunk = file_data[start:end]

        last_packet = make_data_packet(seq, chunk, total_packets)

        while True:
            sock.sendto(last_packet, (args.host, args.port))
            print(f"Sent DATA pkt_index={pkt_index+1}/{total_packets} seq={seq} bytes={len(chunk)}")

            try:
                raw_ack, _ = sock.recvfrom(HEADER_SIZE)
            except socket.timeout:
                retransmissions += 1
                print(f"Timeout waiting for ACK{seq} -> retransmit (total_retx={retransmissions})")
                continue

            try:
                ack = parse_packet(
            except Exception as e:
                retransmissions += 1
                print(f"Failed to parse ACK -> retransmit (err={e}, total_retx={retransmissions})")
                continue

            if not ack["checksum_ok"]:
                retransmissions += 1
                print(f"Corrupt ACK detected -> retransmit (want ACK{seq}, total_retx={retransmissions})")
                continue

            if ack["type"] != PKT_ACK:
                retransmissions += 1
                print(f"Non-ACK packet received -> retransmit (type={ack['type']}, total_retx={retransmissions})")
                continue

            if ack["seq"] != seq:
                retransmissions += 1
                print(f"Wrong ACK: got ACK{ack['seq']}, expected ACK{seq} -> retransmit (total_retx={retransmissions})")
                continue

            print(f"Received valid ACK{ack['seq']} for seq={seq}")
            seq = toggle(seq)
            break

    sock.close()
    print(f"Sender done. retransmissions={retransmissions}")


if __name__ == "__main__":
    main()
