import os
import json
from dotenv import load_dotenv

try:
    import openai
except Exception:
    openai = None

load_dotenv()

INDEX_DIR = os.path.join(os.getcwd(), '.code-connoisseur', 'vectors')
os.makedirs(INDEX_DIR, exist_ok=True)


class VectorStore:
    def __init__(self, api_key=None):
        self.api_key = api_key or os.environ.get('OPENAI_API_KEY')
        if openai and self.api_key:
            openai.api_key = self.api_key

    def get_embedding(self, text):
        if openai and self.api_key:
            try:
                resp = openai.Embedding.create(model='text-embedding-3-small', input=text)
                return resp['data'][0]['embedding']
            except Exception:
                pass
        # fallback: simple character-level vector
        return [float(ord(c)) / 1000.0 for c in text[:1024]]

    def index_directory(self, directory):
        # Simple index: store filename -> embedding JSON files
        for root, dirs, files in os.walk(directory):
            for fname in files:
                if fname.endswith(('.js', '.ts', '.py')):
                    path = os.path.join(root, fname)
                    try:
                        with open(path, 'r', encoding='utf-8') as f:
                            txt = f.read()
                        emb = self.get_embedding(txt)
                        out = {'path': path, 'embedding_len': len(emb)}
                        name = fname + '.json'
                        with open(os.path.join(INDEX_DIR, name), 'w', encoding='utf-8') as g:
                            json.dump(out, g)
                    except Exception:
                        continue


if __name__ == '__main__':
    vs = VectorStore()
    vs.index_directory('.')
    print('Indexed')
