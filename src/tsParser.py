# For TypeScript parsing we fall back to the same heuristic as codeParser
from .codeParser import extract_symbols


def parse_typescript(source):
    return extract_symbols(source)


if __name__ == '__main__':
    print(parse_typescript('function t(){}\nclass T{}'))
