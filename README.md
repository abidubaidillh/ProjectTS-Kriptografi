# Project Tengah Semester
## Kriptografi B

|Nama|NRP|
|-|-|
|Abid Ubaidillah A|5027231089|
***

## Dokumentasi
### 1.  Spesifikasi Algoritma Mini-AES 16-bit

Mini-AES adalah versi sederhana dari algoritma Advanced Encryption Standard (AES) yang digunakan untuk pembelajaran dan simulasi enkripsi blok. Mini-AES memiliki struktur seperti AES, namun menggunakan blok data dan kunci yang jauh lebih kecil, yaitu 16-bit.

### 📦 Ukuran Blok dan Kunci
- **Plaintext (blok data):** 16-bit (4 nibble)
- **Key (kunci awal):** 16-bit (4 nibble)
- **Jumlah Round:** 2 round utama + 1 round awal (mirip AES-128 yang memiliki 10 round)

#### 🔁 Struktur

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

#### 🧠 S-Box (Substitution Box)
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

#### 🗝️ Key Expansion
- **Input:** Kunci 16-bit dibagi menjadi dua word 8-bit (`w0` dan `w1`).
- **Proses:**
  - Menggunakan rotasi dan substitusi nibble.
  - Menggunakan konstanta `RCON = [0x80, 0x30]`.
  - Menghasilkan 3 round key (masing-masing 16-bit).
 
### Implementasi Program
1. Jalankan program menggunakan
   `streamlit run gui.py`
   seperti pada gambar:
   ![image](https://github.com/user-attachments/assets/ed22531f-361a-486b-94f7-240ae41c16ee)

   jika sudah berjalan, kunjungi Streamlit app melalui browser dengan memilih URL yang diberikan
2.. Jika berhasil, tampilannya akan seperti ini:
   ![image](https://github.com/user-attachments/assets/e0798bc3-d1cb-4d97-9ea0-fe643b854440)

3. Setelah itu masukkan plaintext yang ingin di-encrypt dan key-nya. Di sini saya akan mengambil 3 test case:
   - 1. plaintext `abdc` : key `1234`
    
     ![image](https://github.com/user-attachments/assets/14a29565-a586-4158-bee3-9b8658286038)

    Initial State
    Plaintext: `0x1234`
    | Index | Nilai (Hex) | Deskripsi              |
    |-------|-------------|------------------------|
    | 0     | 0x1         | Nibble paling kiri     |
    | 1     | 0x2         | Nibble kedua dari kiri |
    | 2     | 0x3         | Nibble ketiga          |
    | 3     | 0x4         | Nibble paling kanan    |

   Ini adalah **state awal** sebelum dilakukan operasi enkripsi seperti AddRoundKey, SubNibbles, dan seterusnya.

     ![image](https://github.com/user-attachments/assets/49b127e4-ae97-499e-9731-58944f8bfabd)
   
   Round Key 0
   Hasil ekspansi kunci pertama (Round Key 0):
   | Index | Nilai (Hex) |
   |-------|-------------|
   | 0     | 0xA         |
   | 1     | 0xB         |
   | 2     | 0xC         |
   | 3     | 0xD         |
   
   **Representasi:** [0xA, 0xB, 0xC, 0xD]

   After AddRoundKey (Round 0)
   Operasi `AddRoundKey` dilakukan dengan XOR antara plaintext awal dan round key 0:
   | State Sebelum | Round Key 0 | XOR Result (State Baru) |
   |---------------|-------------|--------------------------|
   | 0x1           | 0xA         | 0xB                      |
   | 0x2           | 0xB         | 0x9                      |
   | 0x3           | 0xC         | 0xF                      |
   | 0x4           | 0xD         | 0x9                      |
   
   **State setelah AddRoundKey:** [0xB, 0x9, 0xF, 0x9]

   After SubNibbles (Round 1)
   Operasi `SubNibbles` dilakukan dengan mengganti setiap nibble menggunakan S-Box 4-bit.
   Misalkan S-Box yang digunakan seperti ini (contoh):
   `
   SBOX = [
0x9, 0x4, 0xA, 0xB,
0xD, 0x1, 0x8, 0x5,
0x6, 0x2, 0x0, 0x3,
0xC, 0xE, 0xF, 0x7
]
`
   Maka substitusi dilakukan sebagai berikut:
   | Sebelum | SBOX[Value] | Setelah |
   |---------|-------------|---------|
   | 0xB     | 0x3         | 0x3     |
   | 0x9     | 0x2         | 0x2     |
   | 0xF     | 0x7         | 0x7     |
   | 0x9     | 0x2         | 0x2     |
   
   **State setelah SubNibbles:** [0x3, 0x2, 0x7, 0x2]
   
     ![image](https://github.com/user-attachments/assets/caec700f-e527-4aa2-8f84-bc276c29e660)

   After ShiftRows (Round 1)
   Operasi `ShiftRows` pada Mini-AES 2x2 matrix dilakukan dengan cara **menukar posisi elemen pada baris ke-2** (baris indeks 1):
   Representasi matriks sebelum:
   | 0x3 0x2 | => [0x3, 0x2,
   | 0x7 0x2 | 0x7, 0x2]

   Setelah `ShiftRows`, baris kedua dirotasi ke kiri 1 langkah:
   | 0x3 0x2 |
   | 0x2 0x7 |

   Namun karena hasilnya **tidak berubah urutan dalam array linier**, maka:
   **State tetap:** [0x3, 0x2, 0x7, 0x2]

   After MixColumns (Round 1)
   Operasi `MixColumns` dilakukan menggunakan matriks GF(2⁴). Misalnya seperti:
   |1 4| |s0| |1·s0 ⊕ 4·s2|
   |4 1| * |s2| = |4·s0 ⊕ 1·s2|

   Hitungannya dilakukan dalam field GF(2⁴) dengan irreducible polynomial tertentu, misalnya `x⁴ + x + 1`.
   Asumsikan setelah MixColumns (berdasarkan hasil yang diberikan):
   **State menjadi:** [0xB, 0xE, 0xF, 0xD]

   After AddRoundKey (Round 1)
   Dilakukan operasi XOR terhadap hasil MixColumns dengan **Round Key 1** (yang belum ditampilkan, tetapi hasil akhirnya disediakan).
   Proses:
   | State Sebelumnya | Round Key 1 | XOR Result (State Baru) |
   |------------------|-------------|--------------------------|
   | 0xB              | ?           | 0x7                      |
   | 0xE              | ?           | 0x9                      |
   | 0xF              | ?           | 0xF                      |
   | 0xD              | ?           | 0x7                      |

   Berdasarkan XOR, kemungkinan Round Key 1 = `[0xC, 0x7, 0x0, 0xA]`
   **State setelah AddRoundKey (Round 1):** [0x7, 0x9, 0xF, 0x7]

     ![image](https://github.com/user-attachments/assets/69fb4d88-391f-4150-aa03-ad1a8b0e3975)

     ![image](https://github.com/user-attachments/assets/b5091c9e-ba57-4baf-af22-636f01bbcc5d)

  - 2. plaintext `ffff` : key `ffff`
       ![image](https://github.com/user-attachments/assets/6b1b756f-c018-4124-941e-e64bbc2cc55b)

       ![image](https://github.com/user-attachments/assets/7cab81ab-ac44-4bd0-a59d-3d26f2566f4d)

       ![image](https://github.com/user-attachments/assets/34ecd1ba-e248-4645-afef-dcd4d5b7a5bd)

       ![image](https://github.com/user-attachments/assets/43b2132c-953f-41c4-b68a-3b8d0971cf46)

       ![image](https://github.com/user-attachments/assets/9474ddab-da20-4719-9765-a37fec75a45b)

  - 3. plaintext `1357` : key `2468`
       ![image](https://github.com/user-attachments/assets/a6728fd3-696a-4002-b930-fe51c8756586)

       ![image](https://github.com/user-attachments/assets/39d8aef9-e885-4830-b482-eec4dceb9d04)

       ![image](https://github.com/user-attachments/assets/712cc7aa-ed91-428c-9819-006489d07c91)

       ![image](https://github.com/user-attachments/assets/8b5d1b6b-6b69-4b71-98bc-ea0228ea7c37)

       ![image](https://github.com/user-attachments/assets/ae81f246-79d4-4516-80a2-aa94eaae1ca2)
 
## 🔁 FlowChart
#### Mini-AES
![Screenshot 2025-05-19 132714](https://github.com/user-attachments/assets/290fbdac-c090-4158-aa63-da2673ff3cb4)

#### Key Expansion
![Screenshot 2025-05-19 132750](https://github.com/user-attachments/assets/33064b2b-6277-4fbb-8357-de006befbee7)

##  Analisis: Kelebihan dan Keterbatasan Mini-AES

### Kelebihan

- **Sederhana dan mudah dipahami**
  - Mini-AES hanya menggunakan 4-bit S-Box dan blok 16-bit sehingga cocok untuk pengenalan konsep kriptografi blok cipher.
- **Cocok untuk pembelajaran**
  - Ideal digunakan dalam lingkungan akademik atau latihan algoritma kriptografi dasar karena algoritmanya ringkas dan terstruktur.
- **Implementasi ringan**
  - Tidak membutuhkan sumber daya besar sehingga dapat dijalankan di perangkat terbatas seperti mikrokontroler atau simulasi sederhana.

### Keterbatasan

- **Keamanan sangat rendah**
  - Ukuran kunci dan blok data yang kecil (16-bit) membuatnya mudah diretas dengan brute force atau analisis sederhana.
- **Tidak digunakan dalam aplikasi nyata**
  - Tidak memenuhi standar keamanan modern (seperti AES-128 atau AES-256) karena tidak tahan terhadap serangan kriptanalisis seperti differential dan linear attacks.
- **Struktur terlalu sederhana**
  - Operasi seperti SubNibbles dan ShiftRows sangat terbatas, sehingga tidak cukup kompleks untuk menyulitkan analisa kriptografi tingkat lanjut.

> Mini-AES **tidak dimaksudkan untuk keamanan**, namun sangat bermanfaat sebagai **alat pembelajaran dan demonstrasi** prinsip-prinsip dasar enkripsi blok modern.



