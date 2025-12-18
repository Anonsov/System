import json
import random

if __name__ == "__main__":
    tests = [{"input": [str(round(random.uniform(0.1, 1000.0), 4))]} for _ in range(20)]
    print(json.dumps(tests))
