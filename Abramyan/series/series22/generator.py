import json
import random


def make_case():
    n = random.randint(2, 300)
    arr = [random.uniform(-100.0, 100.0) for _ in range(n)]
    # sometimes descending
    if random.random() < 0.4:
        arr.sort(reverse=True)
    return {"input": [str(n)] + [f"{x}" for x in arr]}


def main():
    random.seed()
    tests = [make_case() for _ in range(25)]
    print(json.dumps(tests))


if __name__ == "__main__":
    main()
