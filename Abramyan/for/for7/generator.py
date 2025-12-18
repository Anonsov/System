import json
import random

if __name__ == "__main__":
    def gen():
        A = random.randint(-1000, 1000)
        B = random.randint(A+1, A+200)
        return {"input": [str(A), str(B)]}
    print(json.dumps([gen() for _ in range(20)]))
