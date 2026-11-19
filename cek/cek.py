import sys
from pathlib import Path
import tree_sitter_python as tspython
from tree_sitter import Language, Parser, Query, QueryCursor

PY = Language(tspython.language())
parser = Parser(PY)

Q_TODO = Query(PY, '((comment) @c (#match? @c "TODO|FIXME"))')
Q_FUNGSI = Query(PY, "(function_definition name: (identifier) @nama) @fungsi")

ABAIKAN_FOLDER = {"venv", ".venv", ".git", "node_modules", "__pycache__"}


def cari_error_pertama(node):
    if node.is_error or node.is_missing:
        return node
    for child in node.children:
        hasil = cari_error_pertama(child)
        if hasil is not None:
            return hasil
    return None


def cek_file(path):
    tree = parser.parse(path.read_bytes())

    # Fitur 1: komentar TODO/FIXME
    for node in sorted(
        QueryCursor(Q_TODO).captures(tree.root_node).get("c", []),
        key=lambda n: n.start_byte,
    ):
        teks = node.text.decode(errors="replace").strip()
        print(f"[TODO/FIXME]     {path}:{node.start_point[0] + 1}: {teks}")

    # Fitur 2: fungsi yang lebih dari 30 baris
    for _, cap in QueryCursor(Q_FUNGSI).matches(tree.root_node):
        if "nama" in cap and "fungsi" in cap:
            nama_node = cap["nama"][0]
            fungsi_node = cap["fungsi"][0]
            jumlah_baris = fungsi_node.end_point[0] - fungsi_node.start_point[0] + 1
            if jumlah_baris > 30:
                nama = nama_node.text.decode(errors="replace")
                baris_awal = fungsi_node.start_point[0] + 1
                print(
                    f"[FUNGSI PANJANG] {path}:{baris_awal}: fungsi '{nama}' ({jumlah_baris} baris)"
                )

    # Fitur 3: file yang pohonnya mengandung error
    if tree.root_node.has_error:
        err_node = cari_error_pertama(tree.root_node)
        baris_err = (err_node.start_point[0] + 1) if err_node else 1
        jenis = "MISSING" if (err_node and err_node.is_missing) else "ERROR"
        print(f"[SYNTAX ERROR]   {path}:{baris_err}: pohon sintaks mengandung {jenis}")


target = Path(sys.argv[1])
daftar_file = [target] if target.is_file() else sorted(target.rglob("*.py"))

for path in daftar_file:
    if any(bagian in ABAIKAN_FOLDER for bagian in path.parts):
        continue
    cek_file(path)
