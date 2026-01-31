import struct

HEADER_FMT = "!III" 
HEADER_SIZE = struct.calcsize(HEADER_FMT)
MAX_PAYLOAD = 1024

def make_packet(seq, payload, total_packets):
    header = struct.pack(HEADER_FMT, seq, len(payload), total_packets)
    return header + payload

def parse_packet(data):
    seq, length, total = struct.unpack(HEADER_FMT, data[:HEADER_SIZE])
    payload = data[HEADER_SIZE:HEADER_SIZE + length]
    return seq, payload, total
