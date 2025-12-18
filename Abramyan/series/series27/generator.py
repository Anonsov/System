import json
import random


def make_case():
    n = random.randint(1, 60)
    arr = [random.uniform(-5.0, 5.0) for _ in range(n)]
    return {"input": [str(n)] + [f"{x}" for x in arr]}


def main():
    random.seed()
    tests = [make_case() for _ in range(25)]
    print(json.dumps(tests))


if __name__ == "__main__":
    main()
