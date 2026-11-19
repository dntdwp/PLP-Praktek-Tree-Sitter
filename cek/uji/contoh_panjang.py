def fungsi_pendek(a, b):
    hasil = a + b
    return hasil


def proses_transaksi_bulanan(daftar_transaksi):
    total_masuk = 0
    total_keluar = 0
    jumlah_valid = 0
    jumlah_gagal = 0
    ringkasan = []

    for item in daftar_transaksi:
        kategori = item.get("kategori", "umum")
        nominal = item.get("nominal", 0)
        status = item.get("status", "pending")

        if status != "selesai":
            jumlah_gagal += 1
            continue

        jumlah_valid += 1
        if kategori == "pemasukan":
            total_masuk += nominal
        else:
            total_keluar += nominal

        ringkasan.append({
            "kategori": kategori,
            "nominal": nominal,
            "saldo_sementara": total_masuk - total_keluar,
        })

    selisih = total_masuk - total_keluar
    rata_rata = selisih / jumlah_valid if jumlah_valid > 0 else 0

    return {
        "total_masuk": total_masuk,
        "total_keluar": total_keluar,
        "selisih": selisih,
        "rata_rata": rata_rata,
        "jumlah_valid": jumlah_valid,
        "jumlah_gagal": jumlah_gagal,
        "ringkasan": ringkasan,
    }
