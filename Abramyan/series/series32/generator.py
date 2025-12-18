import json
import random


def make_case():
    k = random.randint(1, 25)
    sequences = []
    for _ in range(k):
        n = random.randint(1, 60)
        seq = [random.randint(-50, 50) for _ in range(n)]
        sequences.append(seq)

    lines = [str(k)]
    for seq in sequences:
        lines.extend(str(x) for x in seq)
        lines.append("0")
    return {"input": lines}


def main():
    random.seed()
    tests = [make_case() for _ in range(18)]
    print(json.dumps(tests))


if __name__ == "__main__":
    main()
