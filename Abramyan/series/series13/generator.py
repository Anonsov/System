import json
import random


def make_case():
    n = random.randint(1, 400)
    arr = [random.randint(-200, 200) for _ in range(n)]
    arr = [x if x != 0 else -1 for x in arr]
    return {"input": [str(x) for x in arr] + ["0"]}


def main():
    random.seed()
    tests = [make_case() for _ in range(25)]
    print(json.dumps(tests))


if __name__ == "__main__":
    main()
