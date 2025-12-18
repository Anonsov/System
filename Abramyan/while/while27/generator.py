import json, random

def gen_case():
    N = random.randint(1, 10**18)
    return {"input": [str(N)]}

if __name__ == "__main__":
    print(json.dumps([gen_case() for _ in range(20)]))
