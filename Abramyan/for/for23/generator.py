import json, random
if __name__ == "__main__":
    tests = [{"input": [str(round(random.uniform(-3.14159, 3.14159), 6)), str(random.randint(1, 20))]} for _ in range(20)]
    print(json.dumps(tests))
