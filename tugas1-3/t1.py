import tree_sitter_python as tspython
from tree_sitter import Language, Parser

parser = Parser(Language(tspython.language()))

# =====================================================================
# Langkah 4: 3 Potongan Kode Python (Fungsi, If/Else, Class)
# =====================================================================

# 1. Potongan Fungsi
# Perkiraan pohon:
# (module
#   (function_definiton
#     name: (identifier)
#     parameters: (parameters (identifier))
#     body: (block
#       (return_statement (identifier))))
kode_fungsi = b"""def sapa(nama):
    return nama
"""

# 2. Potongan If/Else
# Perkiraan pohon:
# (module
#   (if_statement
#     condition: (comparison_operator (identifier) (integer))
#     consequence: (block (expression_statement (assignment left: (identifier) right: (integer))))
#     alternative: (else_clause body: (block (expression_statement (assignment left: (identifier) right: (integer)))))))
kode_ifelse = b"""if x > 0:
    y = 1
else:
    y = 0
"""

# 3. Potongan Class dengan satu method
# Perkiraan pohon:
# (module
#   (class_definition
#     name: (identifier)
#     body: (block
#       (function_definition
#         name: (identifier)
#         parameters: (parameters (identifier))
#         body: (block (return_statement (identifier)))))))
kode_class = b"""class Mahasiswa:
    def info(self):
        return self
"""

print("=== 1. Pohon Fungsi ===")
tree_fungsi = parser.parse(kode_fungsi)
print(tree_fungsi.root_node)

print("\n=== 2. Pohon If/Else ===")
tree_ifelse = parser.parse(kode_ifelse)
print(tree_ifelse.root_node)

print("\n=== 3. Pohon Class ===")
tree_class = parser.parse(kode_class)
print(tree_class.root_node)

# =====================================================================
# Langkah 5: Node Bernama vs Node Anonim (children vs named_children)
# =====================================================================
print("\n=== 4. Anak-anak function_definition (children) ===")
fn_node = tree_fungsi.root_node.children[0]
for c in fn_node.children:
    print(f"{c.type:15} -> {'bernama' if c.is_named else 'anonim'}")

print("\n=== 5. Anak-anak parameters (children) ===")
params_node = fn_node.child_by_field_name("parameters")
for c in params_node.children:
    print(f"{c.type:15} -> {'bernama' if c.is_named else 'anonim'}")

print("\n=== Perbandingan jumlah children vs named_children ===")
print(f"function_definition: children={len(fn_node.children)}, named_children={len(fn_node.named_children)}")
print(f"parameters         : children={len(params_node.children)}, named_children={len(params_node.named_children)}")
