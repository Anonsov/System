import json
import random

def gen_case():
    A = random.randint(-1000, 1000)
    B = random.randint(A + 1, A + 100)
    return {"input": [str(A), str(B)]}

if __name__ == "__main__":
    tests = [gen_case() for _ in range(20)]
    print(json.dumps(tests))
