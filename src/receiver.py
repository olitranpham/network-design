from socket import *
import argparse
from make_packet import parse_packet, HEADER_SIZE, MAX_PAYLOAD

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--port", type=int, default=9000)
    ap.add_argument("--output", required=True)
    args = ap.parse_args()

    sock = socket(AF_INET, SOCK_DGRAM)
    sock.bind(("", args.port))

    total_packets = None
    packets = None
    received_count = 0

    while True:
        data, _ = sock.recvfrom(HEADER_SIZE + MAX_PAYLOAD)
        seq, payload, total = parse_packet(data)

        if total_packets is None:
            total_packets = total
            packets = [None] * total_packets

        if packets[seq] is None:
            packets[seq] = payload
            received_count += 1
            print(f"Received packet {received_count}/{total_packets}")

        if received_count == total_packets:
            break

    with open(args.output, "wb") as f:
        f.write(b"".join(packets))

    sock.close()
    print("Receiver done")

if __name__ == "__main__":
    main()
