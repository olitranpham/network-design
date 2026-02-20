import random

def maybe_flip_bits(data: bytes, prob: float, rng: random.Random) -> bytes:
    if prob <= 0.0 or len(data) == 0:
        return data
    if rng.random() >= prob:
        return data

    b = bytearray(data)

    # flip 2 random bits
    for _ in range(2):
        i = rng.randrange(len(b))
        b[i] ^= (1 << rng.randrange(8))

    return bytes(b)