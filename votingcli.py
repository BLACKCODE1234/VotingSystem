import json
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
CANDIDATE_FILE = os.path.join(BASE_DIR, 'candidate.json')
VOTES_FILE = os.path.join(BASE_DIR, 'votes.json')


def main():
    candidates = json.load(open(CANDIDATE_FILE))
    votes = json.load(open(VOTES_FILE))

    counts = {c['id']: 0 for c in candidates}
    for v in votes:
        if v['candidate_id'] in counts:
            counts[v['candidate_id']] += 1

    print("Voting Results:")
    for c in candidates:
        print(f"{c['name']}: {counts[c['id']]} votes")


if __name__ == '__main__':
    main()