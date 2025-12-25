import os
import json

FB_PATH = os.path.join(os.getcwd(), '.code-connoisseur', 'feedback.json')


class FeedbackSystem:
    def __init__(self):
        os.makedirs(os.path.dirname(FB_PATH), exist_ok=True)
        if not os.path.exists(FB_PATH):
            with open(FB_PATH, 'w', encoding='utf-8') as f:
                json.dump({'feedback': []}, f)

    def add(self, review_id, score, comment=None):
        with open(FB_PATH, 'r+', encoding='utf-8') as f:
            data = json.load(f)
            data['feedback'].append({'id': review_id, 'score': score, 'comment': comment})
            f.seek(0)
            json.dump(data, f, indent=2)
            f.truncate()

    def summary(self):
        with open(FB_PATH, 'r', encoding='utf-8') as f:
            data = json.load(f)
        fb = data.get('feedback', [])
        if not fb:
            return {'count': 0}
        avg = sum(x.get('score', 0) for x in fb) / len(fb)
        return {'count': len(fb), 'avg_score': avg}


if __name__ == '__main__':
    fb = FeedbackSystem()
    fb.add('r1', 5, 'Nice')
    print(fb.summary())
