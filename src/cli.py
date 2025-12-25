import argparse
import os
from .agent import ReviewAgent
from .vectorStore import VectorStore
from .feedbackSystem import FeedbackSystem

CONFIG_DIR = os.path.join(os.getcwd(), '.code-connoisseur')


def ensure_config_dir():
    os.makedirs(CONFIG_DIR, exist_ok=True)


def main():
    ensure_config_dir()
    parser = argparse.ArgumentParser(prog='code-connoisseur')
    sub = parser.add_subparsers(dest='command')

    sub_index = sub.add_parser('index')
    sub_index.add_argument('-d', '--directory', default='.')

    sub_review = sub.add_parser('review')
    sub_review.add_argument('path')
    sub_review.add_argument('-o', '--old', default=None)

    sub_feedback = sub.add_parser('feedback')

    sub_configure = sub.add_parser('configure')

    args = parser.parse_args()

    if args.command == 'index':
        vs = VectorStore()
        vs.index_directory(args.directory)
        print('Indexing complete.')
    elif args.command == 'review':
        agent = ReviewAgent()
        result = agent.review_path(args.path, old_path=args.old)
        print(result)
    elif args.command == 'feedback':
        fb = FeedbackSystem()
        print(fb.summary())
    elif args.command == 'configure':
        print('Configuration: set OPENAI_API_KEY and optional PINECONE_API_KEY in environment or .env')
    else:
        parser.print_help()
