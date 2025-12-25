import os
from .diffAnalyzer import analyze_diff
from .codeAnalyzer import analyze_code
from .vectorStore import VectorStore
from .feedbackSystem import FeedbackSystem


class ReviewAgent:
    def __init__(self):
        self.vs = VectorStore()
        self.fb = FeedbackSystem()

    def review_path(self, path, old_path=None):
        try:
            if os.path.isdir(path):
                results = {}
                for root, dirs, files in os.walk(path):
                    for f in files:
                        if f.endswith(('.js', '.py', '.ts')):
                            p = os.path.join(root, f)
                            results[p] = self.review_file(p, None)
                return results
            else:
                return self.review_file(path, old_path)
        except Exception as e:
            return {'error': str(e)}

    def review_file(self, path, old_path=None):
        try:
            with open(path, 'r', encoding='utf-8') as f:
                new_text = f.read()
        except Exception as e:
            return {'error': f'Cannot read {path}: {e}'}

        old_text = ''
        if old_path:
            try:
                with open(old_path, 'r', encoding='utf-8') as f:
                    old_text = f.read()
            except Exception:
                old_text = ''

        diff = analyze_diff(old_text, new_text)
        analysis = analyze_code(path)
        embedding = self.vs.get_embedding(new_text)

        review = {
            'path': path,
            'diff': diff,
            'analysis': analysis,
            'embedding_len': len(embedding) if embedding else 0
        }
        return review


if __name__ == '__main__':
    agent = ReviewAgent()
    print(agent.review_file('src/codeParser.py'))
