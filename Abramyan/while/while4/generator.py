import json, random
if __name__ == "__main__":
    tests = [{"input": [str(3**random.randint(0, 20))]} for _ in range(10)]
    tests += [{"input": [str(random.randint(1, 10**6))]} for _ in range(10)]
    print(json.dumps(tests))
