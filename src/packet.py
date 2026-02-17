import struct

PKT_DATA = 0
PKT_ACK  = 1

MAX_PAYLOAD = 1024

HEADER_FMT = "!IIIII"
HEADER_SIZE = struct.calcsize(HEADER_FMT)


def compute_checksum(data: bytes) -> int:
    return sum(data) & 0xFFFFFFFF


def make_data_packet(seq: int, payload: bytes, total_packets: int) -> bytes:
    length = len(payload)
    checksum = compute_checksum(payload)
    header = struct.pack(
        HEADER_FMT,
        PKT_DATA,
        seq,
        length,
        total_packets,
        checksum
    )
    return header + payload


def make_ack_packet(seq: int) -> bytes:
    checksum = compute_checksum(struct.pack("!I", seq))
    header = struct.pack(
        HEADER_FMT,
        PKT_ACK,
        seq,
        0,
        0,
        checksum
    )
    return header


def parse_packet(data: bytes) -> dict:
    if len(data) < HEADER_SIZE:
        raise ValueError("Packet too short")

    pkt_type, seq, length, total_packets, checksum = struct.unpack(
        HEADER_FMT,
        data[:HEADER_SIZE]
    )

    payload = data[HEADER_SIZE:HEADER_SIZE + length]

    if pkt_type == PKT_DATA:
        checksum_ok = compute_checksum(payload) == checksum
    else:
        checksum_ok = compute_checksum(struct.pack("!I", seq)) == checksum

    return {
        "type": pkt_type,
        "seq": seq,
        "length": length,
        "total_packets": total_packets,
        "payload": payload,
        "checksum_ok": checksum_ok,
    }
