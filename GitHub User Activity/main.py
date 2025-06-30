import sys

from utils import Summarizer

if __name__ == "__main__":
    try:
        username = sys.argv[1]
        summarizer = Summarizer()
        summarizer.summarize(username=username)
    except IndexError:
        print("Please Provide a username")
