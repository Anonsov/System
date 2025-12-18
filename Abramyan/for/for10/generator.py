import json
import random

if __name__ == "__main__":
    tests = [{"input": [str(random.randint(1, 10000))]} for _ in range(20)]
    print(json.dumps(tests))
