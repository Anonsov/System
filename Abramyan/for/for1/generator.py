import json
import random

def gen_case():
    K = random.randint(-10**6, 10**6)
    N = random.randint(1, 50)
    return {"input": [str(K), str(N)]}

if __name__ == "__main__":
    tests = [gen_case() for _ in range(20)]
    print(json.dumps(tests))
