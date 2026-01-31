from socket import *
import argparse
from make_packet import make_packet, MAX_PAYLOAD

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--host", default="127.0.0.1")
    ap.add_argument("--port", type=int, default=9000)
    ap.add_argument("--file", required=True)
    args = ap.parse_args()

    with open(args.file, "rb") as f:
        file_data = f.read()

    file_size = len(file_data)

    total_packets = (file_size + MAX_PAYLOAD - 1) // MAX_PAYLOAD

    sock = socket(AF_INET, SOCK_DGRAM)

    for seq in range(total_packets):
        start = seq * MAX_PAYLOAD
        end = min(start + MAX_PAYLOAD, file_size)
        chunk = file_data[start:end]

        packet = make_packet(seq, chunk, total_packets)
        sock.sendto(packet, (args.host, args.port))

        print(f"Sent packet {seq + 1}/{total_packets}")

    sock.close()
    print("Sender done")

if __name__ == "__main__":
    main()
