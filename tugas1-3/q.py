import sys
import tree_sitter_python as tspython
from tree_sitter import Language, Parser, Query, QueryCursor

PY = Language(tspython.language())
parser = Parser(PY)

kode = open(sys.argv[1], "rb").read()
pola = open(sys.argv[2]).read()
tree = parser.parse(kode)

query = Query(PY, pola)

# Langkah 4: jika query menangkap pasangan @nama dan @params, gunakan matches()
if "@nama" in pola and "@params" in pola:
    for _, cap in QueryCursor(query).matches(tree.root_node):
        if "nama" in cap and "params" in cap:
            nama_node = cap["nama"][0]
            nama = nama_node.text.decode()
            jumlah = cap["params"][0].named_child_count
            print(f"baris {nama_node.start_point[0] + 1:3d}: {nama} ({jumlah} parameter)")
else:
    hasil = QueryCursor(query).captures(tree.root_node)
    for nama, nodes in hasil.items():
        for n in sorted(nodes, key=lambda x: x.start_byte):
            print(f"@{nama}  baris {n.start_point[0] + 1}: {n.text.decode()}")
