import json
import random


def make_case():
    n = random.randint(1, 200)
    # build sorted ascending array
    arr = sorted(random.uniform(-100.0, 100.0) for _ in range(n))
    b = random.uniform(-120.0, 120.0)
    return {"input": [f"{b}", str(n)] + [f"{x}" for x in arr]}


def main():
    random.seed()
    tests = [make_case() for _ in range(20)]
    print(json.dumps(tests))


if __name__ == "__main__":
    main()
