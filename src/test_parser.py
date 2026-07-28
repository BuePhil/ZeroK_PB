from ice_parser import parser
from pathlib import Path
import sys
import ast
import astpretty
from anytree import Node, RenderTree

def ast_to_tree(obj, parent=None, name="root"):
    node = Node(name, parent=parent)

    if isinstance(obj, tuple):
        for i, item in enumerate(obj):
            child_name = str(item) if not isinstance(item, (tuple, list)) else f"[{i}]"
            ast_to_tree(item, node, child_name)

    elif isinstance(obj, list):
        for i, item in enumerate(obj):
            ast_to_tree(item, node, f"stmt_{i}")

    return node

file_path = Path(sys.argv[1])

if file_path.suffix == ".zk":
    file_content = open(file_path, 'r').read()

    print(file_content)
    result = parser.parse(file_content)
    print(result)
    
    root = ast_to_tree(result)

    for pre, _, node in RenderTree(root):
        print(f"{pre}{node.name}")

else:
    print("Unkown file extension")