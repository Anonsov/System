import json
import random


def make_case():
    n = random.randint(2, 400)
    arr = [random.randint(-50, 50) for _ in range(n)]
    # force at least two zeros
    if n >= 2:
        arr[random.randrange(n)] = 0
        arr[random.randrange(n)] = 0
    return {"input": [str(n)] + [str(x) for x in arr]}


def main():
    random.seed()
    tests = [make_case() for _ in range(20)]
    print(json.dumps(tests))


if __name__ == "__main__":
    main()
