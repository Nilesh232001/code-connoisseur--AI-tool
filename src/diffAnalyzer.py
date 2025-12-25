import difflib


def analyze_diff(old_text, new_text):
    old_lines = old_text.splitlines(keepends=True)
    new_lines = new_text.splitlines(keepends=True)
    diff = list(difflib.unified_diff(old_lines, new_lines, lineterm=''))
    stats = {
        'added': sum(1 for l in diff if l.startswith('+') and not l.startswith('+++')),
        'removed': sum(1 for l in diff if l.startswith('-') and not l.startswith('---')),
        'diff': ''.join(diff)
    }
    return stats


if __name__ == '__main__':
    a = 'a\nb\nc\n'
    b = 'a\nB\nc\nd\n'
    print(analyze_diff(a, b))
