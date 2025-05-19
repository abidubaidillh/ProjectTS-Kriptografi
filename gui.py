import streamlit as st
from mini_aes import (
    key_expansion, sub_nibbles, shift_rows, mix_columns, add_round_key,
    decrypt  # pastikan fungsi decrypt sudah ada di mini_aes.py
)

def encrypt(plaintext, key):
    round_keys = key_expansion(key)

    state = [
        (plaintext >> 12) & 0xF,
        (plaintext >> 8) & 0xF,
        (plaintext >> 4) & 0xF,
        plaintext & 0xF
    ]

    st.write("Initial State:", [hex(n) for n in state])
    st.write("Round Key 0:", [hex(k) for k in round_keys[0]])

    # Round 0 - AddRoundKey
    state = add_round_key(state, round_keys[0])
    st.write("After AddRoundKey (Round 0):", [hex(n) for n in state])

    # Round 1
    state = sub_nibbles(state)
    st.write("After SubNibbles (Round 1):", [hex(n) for n in state])

    state = shift_rows(state)
    st.write("After ShiftRows (Round 1):", [hex(n) for n in state])

    state = mix_columns(state)
    st.write("After MixColumns (Round 1):", [hex(n) for n in state])

    state = add_round_key(state, round_keys[1])
    st.write("After AddRoundKey (Round 1):", [hex(n) for n in state])
    st.write("Round Key 1:", [hex(k) for k in round_keys[1]])

    # Round 2
    state = sub_nibbles(state)
    st.write("After SubNibbles (Round 2):", [hex(n) for n in state])

    state = shift_rows(state)
    st.write("After ShiftRows (Round 2):", [hex(n) for n in state])

    state = add_round_key(state, round_keys[2])
    st.write("After AddRoundKey (Round 2):", [hex(n) for n in state])
    st.write("Round Key 2:", [hex(k) for k in round_keys[2]])

    ciphertext = (state[0] << 12) | (state[1] << 8) | (state[2] << 4) | state[3]
    st.write("Ciphertext (hex):", hex(ciphertext))

    return ciphertext

st.title("Mini AES 16-bit Encryption / Decryption")

# Menerima Input: Plaintext (16-bit) dan key (16-bit)
plaintext = st.text_input("Plaintext (4 hex digit, e.g. 1234):", "1234")
key = st.text_input("Key (4 hex digit, e.g. abcd):", "abcd")

col1, col2 = st.columns(2)

with col1:
    if st.button("Encrypt"):
        try:
            pt_int = int(plaintext, 16)
            key_int = int(key, 16)
            ct_int = encrypt(pt_int, key_int)
            # Mengeluarkan Output: Ciphertext (16-bit)
            st.success(f"Ciphertext: {ct_int:04x}")
        except ValueError:
            st.error("Masukkan harus dalam format hexadecimal 4 digit (contoh: 1234, abcd)")

with col2:
    if st.button("Decrypt"):
        try:
            ct_int = int(plaintext, 16)  # plaintext input dianggap ciphertext saat dekripsi
            key_int = int(key, 16)
            pt_int = decrypt(ct_int, key_int)
            st.success(f"Plaintext: {pt_int:04x}")
        except ValueError:
            st.error("Masukkan harus dalam format hexadecimal 4 digit (contoh: 1234, abcd)")