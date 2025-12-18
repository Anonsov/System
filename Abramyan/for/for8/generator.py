import json
import random

if __name__ == "__main__":
    def gen():
        A = random.randint(1, 10)  # keep small to avoid overflow/timeout
        B = random.randint(A+1, A+8)
        return {"input": [str(A), str(B)]}
    print(json.dumps([gen() for _ in range(20)]))
