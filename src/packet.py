import struct
import zlib

PKT_DATA = 0
PKT_ACK = 1
PKT_SYN = 2
PKT_SYN_ACK = 3
PKT_FIN = 4
PKT_FIN_ACK = 5

MAX_PAYLOAD = 1024

HEADER_FMT = "!BIIHHII"
HEADER_SIZE = struct.calcsize(HEADER_FMT)


def compute_checksum(data: bytes) -> int:
    return zlib.crc32(data) & 0xFFFFFFFF


def _checksum_bytes(pkt_type: int, seq: int, ack: int, rwnd: int,
                    length: int, total_packets: int, payload: bytes) -> bytes:
    return struct.pack(
        "!BIIHHI",
        pkt_type,
        seq,
        ack,
        rwnd,
        length,
        total_packets
    ) + payload


def make_packet(pkt_type: int, seq: int = 0, ack: int = 0, rwnd: int = 0,
                payload: bytes = b"", total_packets: int = 0) -> bytes:
    length = len(payload)

    if length > MAX_PAYLOAD:
        raise ValueError(f"Payload too large: {length} > {MAX_PAYLOAD}")

    checksum = compute_checksum(
        _checksum_bytes(pkt_type, seq, ack, rwnd, length, total_packets, payload)
    )

    header = struct.pack(
        HEADER_FMT,
        pkt_type,
        seq,
        ack,
        rwnd,
        length,
        total_packets,
        checksum
    )

    return header + payload


def make_data_packet(seq: int, payload: bytes, total_packets: int) -> bytes:
    return make_packet(PKT_DATA, seq=seq, payload=payload, total_packets=total_packets)


def make_ack_packet(ack: int, rwnd: int = 16) -> bytes:
    return make_packet(PKT_ACK, ack=ack, rwnd=rwnd)


def make_syn_packet() -> bytes:
    return make_packet(PKT_SYN)


def make_syn_ack_packet(rwnd: int = 16) -> bytes:
    return make_packet(PKT_SYN_ACK, rwnd=rwnd)


def make_fin_packet(seq: int = 0) -> bytes:
    return make_packet(PKT_FIN, seq=seq)


def make_fin_ack_packet(ack: int = 0) -> bytes:
    return make_packet(PKT_FIN_ACK, ack=ack)


def parse_packet(data: bytes) -> dict:
    if len(data) < HEADER_SIZE:
        raise ValueError("Packet too short")

    pkt_type, seq, ack, rwnd, length, total_packets, checksum = struct.unpack(
        HEADER_FMT,
        data[:HEADER_SIZE]
    )

    if length < 0 or length > MAX_PAYLOAD:
        raise ValueError("Invalid payload length")

    if len(data) < HEADER_SIZE + length:
        raise ValueError("Truncated packet")

    payload = data[HEADER_SIZE:HEADER_SIZE + length]

    checksum_ok = (
        compute_checksum(
            _checksum_bytes(pkt_type, seq, ack, rwnd, length, total_packets, payload)
        ) == checksum
    )

    return {
        "type": pkt_type,
        "seq": seq,
        "ack": ack,
        "rwnd": rwnd,
        "length": length,
        "total_packets": total_packets,
        "payload": payload,
        "checksum_ok": checksum_ok,
    }
