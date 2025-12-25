import subprocess
import json
import shutil
import os
from .pythonParser import parse_python


def run_eslint(path):
    if shutil.which('eslint'):
        try:
            out = subprocess.check_output(['eslint', path, '--format', 'json'], stderr=subprocess.DEVNULL)
            return json.loads(out)
        except Exception:
            return None
    return None


def analyze_code(path):
    info = {'path': path, 'issues': [], 'symbols': {}}
    try:
        with open(path, 'r', encoding='utf-8') as f:
            text = f.read()
        if path.endswith('.py'):
            info['symbols'] = parse_python(text)
        else:
            # fallback: simple symbol extraction
            from .codeParser import extract_symbols
            info['symbols'] = extract_symbols(text)
        lint = run_eslint(path)
        if lint:
            info['issues'] = lint
        else:
            # basic checks
            if 'console.' in text:
                info['issues'].append({'type': 'debug', 'message': 'console statements present'})
    except Exception as e:
        info['error'] = str(e)
    return info


if __name__ == '__main__':
    print(analyze_code('src/codeParser.py'))
