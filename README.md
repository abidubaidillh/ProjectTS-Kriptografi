## 🔐 Spesifikasi Algoritma Mini-AES 16-bit

Mini-AES adalah versi sederhana dari algoritma Advanced Encryption Standard (AES) yang digunakan untuk pembelajaran dan simulasi enkripsi blok. Mini-AES memiliki struktur seperti AES, namun menggunakan blok data dan kunci yang jauh lebih kecil, yaitu 16-bit.

### 📦 Ukuran Blok dan Kunci
- **Plaintext (blok data):** 16-bit (4 nibble)
- **Key (kunci awal):** 16-bit (4 nibble)
- **Jumlah Round:** 2 round utama + 1 round awal (mirip AES-128 yang memiliki 10 round)

### 🔁 Struktur Enkripsi

#### Round 0 (Initial Round)
- **AddRoundKey:** XOR antara plaintext dan round key pertama.

#### Round 1
- **SubNibbles:** Substitusi setiap nibble menggunakan S-Box 4-bit.
- **ShiftRows:** Pertukaran posisi nibble (untuk mini-AES: hanya menukar nibble ke-2 dan ke-4).
- **MixColumns:** Operasi linier menggunakan matriks GF(2⁴) untuk difusi data.
- **AddRoundKey:** XOR dengan round key kedua.

#### Round 2 (Final Round)
- **SubNibbles:** Substitusi ulang menggunakan S-Box.
- **ShiftRows:** Pergeseran nibble kembali.
- **AddRoundKey:** XOR dengan round key ketiga.

### 🧠 S-Box (Substitution Box)
Menggunakan S-Box 4-bit berikut untuk substitusi:

| Input | Output |
|-------|--------|
| 0x0   | 0x9    |
| 0x1   | 0x4    |
| 0x2   | 0xA    |
| 0x3   | 0xB    |
| 0x4   | 0xD    |
| 0x5   | 0x1    |
| 0x6   | 0x8    |
| 0x7   | 0x5    |
| 0x8   | 0x6    |
| 0x9   | 0x2    |
| 0xA   | 0x0    |
| 0xB   | 0x3    |
| 0xC   | 0xC    |
| 0xD   | 0xE    |
| 0xE   | 0xF    |
| 0xF   | 0x7    |

### 🗝️ Key Expansion
- **Input:** Kunci 16-bit dibagi menjadi dua word 8-bit (`w0` dan `w1`).
- **Proses:**
  - Menggunakan rotasi dan substitusi nibble.
  - Menggunakan konstanta `RCON = [0x80, 0x30]`.
  - Menghasilkan 3 round key (masing-masing 16-bit).

