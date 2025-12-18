import json
import random


def make_case():
    k = random.randint(1, 20)
    ns = [random.randint(1, 40) for _ in range(k)]
    arr = [random.randint(-50, 50) for _ in range(sum(ns))]
    lines = [str(k)] + [str(x) for x in ns] + [str(x) for x in arr]
    return {"input": lines}


def main():
    random.seed()
    tests = [make_case() for _ in range(20)]
    print(json.dumps(tests))


if __name__ == "__main__":
    main()
