from ice_lexer import lexer
from pathlib import Path
import sys

file_path = Path(sys.argv[1])

if file_path.suffix == ".zk":
    file_content = open(file_path, 'r').read()

    print(file_content)
    lexer.input(file_content)
    while True:
        tok = lexer.token()
        if not tok:
            break      
        print(tok)
else:
    print("Unkown file extension")