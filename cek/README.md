# Tugas 6 — Mini Proyek: Pendeteksi TODO, Fungsi Panjang, dan Error Sintaks (`cek.py`)

CLI berbasis `tree-sitter` untuk memindai folder atau berkas kode sumber Python (`.py`) dan melaporkan:
1. **`[TODO/FIXME]`**: Komentar yang mengandung kata `TODO` atau `FIXME` (menggunakan query `((comment) @c (#match? @c "TODO|FIXME"))`).
2. **`[FUNGSI PANJANG]`**: Semua fungsi/method (termasuk fungsi di dalam class maupun fungsi bersarang) yang panjangnya **lebih dari 30 baris** (`end_point[0] - start_point[0] + 1 > 30`).
3. **`[SYNTAX ERROR]`**: File Python yang pohon sintaksnya mengandung node `ERROR` atau `MISSING` (`tree.root_node.has_error`), beserta nomor baris lokasi error pertama.

Folder lingkungan seperti `venv/`, `.venv/`, `.git/`, `node_modules/`, dan `__pycache__/` otomatis dilewati.

---

## 1. Instalasi Dependensi

Pastikan Python 3.10+ sudah terpasang, lalu instal paket `tree-sitter` dan `tree-sitter-python`:

```bash
pip install tree-sitter tree-sitter-python
```

---

## 2. Cara Menjalankan

Jalankan pada sebuah folder (rekursif untuk seluruh `*.py`) atau pada satu file Python:

```bash
python cek/cek.py <path_folder_atau_file>
```

Contoh menjalankan pada folder uji lokal:

```bash
python cek/cek.py cek/uji/
```

---

## 3. Contoh Output pada Folder `cek/uji/`

```text
[FUNGSI PANJANG] cek\uji\contoh_panjang.py:6: fungsi 'proses_transaksi_bulanan' (40 baris)
[SYNTAX ERROR]   cek\uji\contoh_rusak.py:4: pohon sintaks mengandung ERROR
[TODO/FIXME]     cek\uji\contoh_todo.py:3: # TODO: ambil tarif pajak dari konfigurasi database
[TODO/FIXME]     cek\uji\contoh_todo.py:5: # FIXME: tangani pembulatan desimal untuk mata uang Rupiah
```

---

## 4. Pengujian & Verifikasi Manual pada Repositori Nyata (`pallets/click`)

Skrip diuji pada repositori open-source Python [`pallets/click`](https://github.com/pallets/click):

```bash
git clone --depth 1 https://github.com/pallets/click.git
python cek/cek.py click/src/click
```

### Pengecekan Manual pada 2 File Acak:

1. **`src/click/_textwrap.py` (102 baris)**:
   - **Output `cek.py`**:
     ```text
     [FUNGSI PANJANG] click\src\click\_textwrap.py:20: fungsi '_wrap_chunks' (57 baris)
     ```
   - **Verifikasi Manual**:
     - `_wrap_chunks`: baris 20 s.d. baris 76 (`76 - 20 + 1 = 57` baris, **> 30 baris** — **Cocok**).
     - `extra_indent`: baris 79 s.d. baris 89 (`11` baris, <= 30 baris).
     - `indent_only`: baris 91 s.d. baris 102 (`12` baris, <= 30 baris).
     - Tidak ada komentar `TODO`/`FIXME` dan tidak ada error sintaks.

2. **`src/click/formatting.py` (329 baris)**:
   - **Output `cek.py`**:
     ```text
     [FUNGSI PANJANG] click\src\click\formatting.py:31: fungsi 'wrap_text' (86 baris)
     [FUNGSI PANJANG] click\src\click\formatting.py:167: fungsi 'write_usage' (45 baris)
     [FUNGSI PANJANG] click\src\click\formatting.py:238: fungsi 'write_dl' (43 baris)
     ```
   - **Verifikasi Manual**:
     - `measure_table` (baris 14–21, 8 baris) & `iter_rows` (baris 24–28, 5 baris): <= 30 baris.
     - `wrap_text` (baris 31–116): `116 - 31 + 1 = 86` baris (**> 30 baris** — **Cocok**).
     - `HelpFormatter.write_usage` (baris 167–211): `211 - 167 + 1 = 45` baris (**> 30 baris** — **Cocok**).
     - `HelpFormatter.write_dl` (baris 238–280): `280 - 238 + 1 = 43` baris (**> 30 baris** — **Cocok**).
     - Fungsi/method lainnya (`__init__`, `write`, `indent`, `dedent`, `write_heading`, `write_paragraph`, `write_text`, `section`, `indentation`, `getvalue`, `join_options`) semuanya <= 30 baris.
