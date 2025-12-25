import ast


def parse_python(source):
    tree = ast.parse(source)
    symbols = {'functions': [], 'classes': []}
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            symbols['functions'].append(node.name)
        elif isinstance(node, ast.ClassDef):
            symbols['classes'].append(node.name)
    return symbols


if __name__ == '__main__':
    s = 'def f():\n    pass\nclass C: pass\n'
    print(parse_python(s))
