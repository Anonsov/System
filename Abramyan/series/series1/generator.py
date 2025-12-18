import json
import random


def make_case():
    nums = [random.uniform(-100.0, 100.0) for _ in range(10)]
    return {"input": [f"{x}" for x in nums]}


def main():
    random.seed()
    tests = [make_case() for _ in range(20)]
    print(json.dumps(tests))


if __name__ == "__main__":
    main()
