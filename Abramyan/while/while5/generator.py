import json, random
if __name__ == "__main__":
    ks = [random.randint(0, 30) for _ in range(20)]
    tests = [{"input": [str(1<<k)]} for k in ks]
    print(json.dumps(tests))
