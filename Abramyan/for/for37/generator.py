import json, random
if __name__ == "__main__":
    tests = [{"input": [str(random.randint(1, 50))]} for _ in range(20)]
    print(json.dumps(tests))
