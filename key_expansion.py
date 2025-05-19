# key_expansion.py

SBOX = [0x9, 0x4, 0xA, 0xB,
        0xD, 0x1, 0x8, 0x5,
        0x6, 0x2, 0x0, 0x3,
        0xC, 0xE, 0xF, 0x7]

RCON = [0b10000000, 0b00110000, 0b10100000]  # contoh Rcon untuk 3 round

def key_expansion(key):
    w = [0] * 6  # 6 word (masing-masing 8 bit)
    w[0] = (key >> 8) & 0xFF
    w[1] = key & 0xFF

    for i in range(2, 6):
        if i % 2 == 0:
            temp = w[i - 1]
            # RotNib
            temp = ((temp & 0x0F) << 4) | ((temp & 0xF0) >> 4)
            # SubNib
            temp = (SBOX[(temp >> 4) & 0xF] << 4) | SBOX[temp & 0xF]
            # XOR RCON
            temp ^= RCON[(i // 2) - 1]
        else:
            temp = w[i - 1]
        w[i] = w[i - 2] ^ temp

    round_keys = [
        (w[0] << 8) | w[1],
        (w[2] << 8) | w[3],
        (w[4] << 8) | w[5],
        # Tambahkan 1 round key tambahan untuk final AddRoundKey
    ]
    return round_keys