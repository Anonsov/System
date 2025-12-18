import json
import random


def make_case():
    k = random.randint(1, 25)
    n = random.randint(1, 60)
    arr = [random.randint(-50, 50) for _ in range(k * n)]
    return {"input": [str(k), str(n)] + [str(x) for x in arr]}


def main():
    random.seed()
    tests = [make_case() for _ in range(20)]
    print(json.dumps(tests))


if __name__ == "__main__":
    main()
