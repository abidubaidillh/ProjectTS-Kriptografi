# main.py

from mini_aes import sub_nibbles, shift_rows, mix_columns, add_round_key
from key_expansion import key_expansion

def encrypt(plaintext, key):
    state = [(plaintext >> 12) & 0xF, (plaintext >> 8) & 0xF,
             (plaintext >> 4) & 0xF, plaintext & 0xF]

    round_keys = key_expansion(key)

    print(f"Initial State: {state}")
    state = add_round_key(state, round_keys[0])
    print(f"After AddRoundKey (Initial): {state}")

    for r in range(1, 4):
        state = sub_nibbles(state)
        state = shift_rows(state)
        if r != 3:
            state = mix_columns(state)
        state = add_round_key(state, round_keys[r])
        print(f"After Round {r}: {state}")

    ciphertext = (state[0] << 12) | (state[1] << 8) | (state[2] << 4) | state[3]
    return ciphertext

if __name__ == "__main__":
    pt_hex = input("Masukkan plaintext (hex): ")
    key_hex = input("Masukkan key (hex): ")

    pt = int(pt_hex, 16)
    key = int(key_hex, 16)

    ct = encrypt(pt, key)
    print(f"Ciphertext (hex): {hex(ct)}")