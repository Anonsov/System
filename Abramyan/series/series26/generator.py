import json
import random


def make_case():
    k = random.randint(1, 8)
    n = random.randint(1, 120)
    arr = [random.uniform(-10.0, 10.0) for _ in range(n)]
    return {"input": [str(k), str(n)] + [f"{x}" for x in arr]}


def main():
    random.seed()
    tests = [make_case() for _ in range(20)]
    print(json.dumps(tests))


if __name__ == "__main__":
    main()
