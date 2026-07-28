from ice_lexer import lexer
from ice_parser import parser
from interpreter import interpret
from typechecker import ty_expr
from pathlib import Path
import sys
from anytree import Node, RenderTree

def main(code):
    print(f"Code > {code}")
    try:
        ast = parser.parse(code)
        show_tree(ast)

        #ty = ty_expr(ast)
        value = interpret(ast)
    except EOFError:
        print("whoops!!!!!!")
    
    #print(f"Type, value > {value}",end=3*"\n")
    print(f'\n\nProgram terminated succesfully', end=3*"\n")

def show_tree(ast):
    root = ast_to_tree(ast)

    for pre, _, node in RenderTree(root):
        print(f"{pre}{node.name}")


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

    main(file_content)
else:
    print("Unkown file extension")

'''while True:
    try:
        s=input()
    except EOFError:
        break
    if not s : continue

    result = s
    main(result)'''