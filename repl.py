import sys

sys.path.insert(0, "./src")

from ice_parser import parser
from interpreter import interpret
from typechecker import typecheck
from pathlib import Path
from anytree import Node, RenderTree


def run(code, show_ast=False):
    """Führt ein Stück Code aus - Parsen, Typecheck, Interpretieren."""
    ast = parser.parse(code)
    if show_ast:
        show_tree(ast)
    try:
        typecheck(ast)
        interpret(ast)
    except TypeError as ty_err:
        print(f"Error: Type Issue '{ty_err}'")
    except EOFError:
        print("whoops!!!!!!")


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


def run_file(path):
    file_path = Path(path)
    if file_path.suffix != ".zk":
        print("Unknown file extension")
        return
    code = file_path.read_text()
    print(f"Code > {code}")
    run(code, show_ast=True)


def run_repl():
    print("zeroK REPL - Eingabe abschließen mit einer leeren Zeile.")
    print("Befehle: 'load <pfad.zk>' zum Ausführen einer Datei, 'exit' zum Beenden.\n")

    while True:
        try:
            first_line = input(">>> ")
        except EOFError:
            print()
            break

        stripped = first_line.strip()
        if stripped in ("exit", "quit"):
            break
        if stripped == "":
            continue
        if stripped.startswith("load "):
            path = stripped[len("load "):].strip()
            run_file(path)
            continue

        # Mehrzeiligen Statement-Block einsammeln, bis leere Zeile kommt
        lines = [first_line]
        while True:
            try:
                line = input("... ")
            except EOFError:
                break
            if line.strip() == "":
                break
            lines.append(line)

        code = "\n".join(lines)
        try:
            run(code, show_ast=True)
        except Exception as e:
            print(f"Fehler: {e}")


def main():
    if len(sys.argv) > 1:
        run_file(sys.argv[1])
    else:
        run_repl()


if __name__ == "__main__":
    main()