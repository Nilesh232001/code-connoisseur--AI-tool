import re

FUNC_RE = re.compile(r'(?:function\s+([\w$]+)\s*\(|([\w$]+)\s*=\s*\([^)]*\)\s*=>)')
CLASS_RE = re.compile(r'class\s+([\w$]+)')


def extract_symbols(js_text):
    """Very small heuristic extractor for JS/TS: returns functions and classes."""
    functions = set()
    classes = set()
    for m in FUNC_RE.finditer(js_text):
        name = m.group(1) or m.group(2)
        if name:
            functions.add(name)
    for m in CLASS_RE.finditer(js_text):
        classes.add(m.group(1))
    return {'functions': sorted(list(functions)), 'classes': sorted(list(classes))}


if __name__ == '__main__':
    sample = 'function foo(){}\nconst bar = () => {}\nclass Baz {}\n'
    print(extract_symbols(sample))
