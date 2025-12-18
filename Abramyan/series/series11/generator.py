import json
import random


def make_case():
    k = random.randint(-100, 100)
    n = random.randint(1, 300)
    arr = [random.randint(-200, 200) for _ in range(n)]
    return {"input": [str(k), str(n)] + [str(x) for x in arr]}


def main():
    random.seed()
    tests = [make_case() for _ in range(20)]
    print(json.dumps(tests))


if __name__ == "__main__":
    main()
