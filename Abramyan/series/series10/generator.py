import json
import random


def make_case():
    n = random.randint(1, 400)
    arr = [random.randint(-1000, 1000) for _ in range(n)]
    # ensure mix sometimes
    if random.random() < 0.3:
        arr[random.randrange(n)] = random.randint(1, 1000)
    return {"input": [str(n)] + [str(x) for x in arr]}


def main():
    random.seed()
    tests = [make_case() for _ in range(20)]
    print(json.dumps(tests))


if __name__ == "__main__":
    main()
