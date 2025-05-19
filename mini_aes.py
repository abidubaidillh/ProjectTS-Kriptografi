# mini_aes.py

SBOX = {
    0x0: 0x9, 0x1: 0x4, 0x2: 0xA, 0x3: 0xB,
    0x4: 0xD, 0x5: 0x1, 0x6: 0x8, 0x7: 0x5,
    0x8: 0x6, 0x9: 0x2, 0xA: 0x0, 0xB: 0x3,
    0xC: 0xC, 0xD: 0xE, 0xE: 0xF, 0xF: 0x7
}

# SubNibbles (S-Box 4-bit)
def sub_nibbles(state):
    return [SBOX[n] for n in state]

# ShiftRows
def shift_rows(state):
    # Swap second row elements (indexes 1 and 3)
    return [state[0], state[3], state[2], state[1]]

def mix_columns(state):
    def mult(a, b):
        """Multiply two elements in GF(2^4) with irreducible polynomial x^4 + x + 1 (0x13)."""
        p = 0
        for _ in range(4):
            if b & 1:
                p ^= a
            carry = a & 0x8  # check highest bit of 4-bit nibble
            a <<= 1
            if carry:
                a ^= 0x13  # modulo polynomial x^4 + x + 1
            b >>= 1
        return p & 0xF  # keep 4 bits only

    # Mix columns using the matrix [[1,4],[4,1]]
    return [
        mult(1, state[0]) ^ mult(4, state[1]),
        mult(4, state[0]) ^ mult(1, state[1]),
        mult(1, state[2]) ^ mult(4, state[3]),
        mult(4, state[2]) ^ mult(1, state[3])
    ]

# AddRoundKey
def add_round_key(state, round_key):
    return [s ^ k for s, k in zip(state, round_key)]

def key_expansion(key):
    w = [0] * 6
    # Key awal 16-bit
    w[0] = (key >> 8) & 0xFF
    w[1] = key & 0xFF
    RCON = [0x80, 0x30]

    def rot_nib(b):
        return ((b & 0x0F) << 4) | ((b & 0xF0) >> 4)

    def sub_nib(b):
        return (SBOX[(b >> 4) & 0xF] << 4) | SBOX[b & 0xF]

    # Algoritma key expansion sederhana untuk menghasilkan round keys 
    for i in range(2):
        temp = sub_nib(rot_nib(w[2*i + 1]))
        w[2 + 2*i] = w[2*i] ^ RCON[i] ^ temp
        w[3 + 2*i] = w[2 + 2*i] ^ w[2*i + 1]

    round_keys = []
    for i in range(0, 6, 2):
        key_16bit = (w[i] << 8) | w[i+1]
        round_keys.append([
            (key_16bit >> 12) & 0xF,
            (key_16bit >> 8) & 0xF,
            (key_16bit >> 4) & 0xF,
            key_16bit & 0xF
        ])

    return round_keys

# Fungsi inverse SBOX untuk dekripsi
INV_SBOX = {v: k for k, v in SBOX.items()}

def inv_sub_nibbles(state):
    return [INV_SBOX[n] for n in state]

def inv_shift_rows(state):
    # Inverse shift rows (balikkan operasi shift_rows)
    return [state[0], state[3], state[2], state[1]]

def inv_mix_columns(state):
    def mult(a, b):  # GF(2^4) multiplication (sama dengan fungsi mix_columns)
        p = 0
        for _ in range(4):
            if b & 1:
                p ^= a
            carry = a & 0x8
            a <<= 1
            if carry:
                a ^= 0x13
            b >>= 1
        return p & 0xF

    # Koefisien untuk inverse mix columns di Mini AES (misal 9 dan 2, bisa disesuaikan)
    return [
        mult(9, state[0]) ^ mult(2, state[1]),
        mult(9, state[1]) ^ mult(2, state[0]),
        mult(9, state[2]) ^ mult(2, state[3]),
        mult(9, state[3]) ^ mult(2, state[2])
    ]

def decrypt(ciphertext, key):
    round_keys = key_expansion(key)

    state = [
        (ciphertext >> 12) & 0xF,
        (ciphertext >> 8) & 0xF,
        (ciphertext >> 4) & 0xF,
        ciphertext & 0xF
    ]

    state = add_round_key(state, round_keys[2])
    state = inv_shift_rows(state)
    state = inv_sub_nibbles(state)
    state = add_round_key(state, round_keys[1])
    state = inv_mix_columns(state)
    state = inv_shift_rows(state)
    state = inv_sub_nibbles(state)
    state = add_round_key(state, round_keys[0])

    plaintext = (state[0] << 12) | (state[1] << 8) | (state[2] << 4) | state[3]
    return plaintext
