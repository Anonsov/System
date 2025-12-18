import json
import random


def make_case():
    n = random.randint(3, 250)
    arr = [random.uniform(-100.0, 100.0) for _ in range(n)]
    # sometimes generate sawtooth
    if random.random() < 0.35:
        base = random.uniform(-50.0, 50.0)
        step = random.uniform(0.5, 5.0)
        arr = [base + ((-1) ** i) * step * random.uniform(0.8, 1.2) for i in range(n)]
    return {"input": [str(n)] + [f"{x}" for x in arr]}


def main():
    random.seed()
    tests = [make_case() for _ in range(25)]
    print(json.dumps(tests))


if __name__ == "__main__":
    main()
