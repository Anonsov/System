import json
import random


def make_case():
    # Avoid zeros too often so product isn't trivially 0
    nums = [random.uniform(-5.0, 5.0) for _ in range(10)]
    return {"input": [f"{x}" for x in nums]}


def main():
    random.seed()
    tests = [make_case() for _ in range(20)]
    print(json.dumps(tests))


if __name__ == "__main__":
    main()
