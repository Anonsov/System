import json, random

def gen_case():
    A = random.randint(1, 10**12)
    B = random.randint(1, 10**12)
    return {"input": [str(A), str(B)]}

if __name__ == "__main__":
    print(json.dumps([gen_case() for _ in range(20)]))
