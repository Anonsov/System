import json, random

def gen_case():
    A = round(random.uniform(1.1, 10.0), 6)
    return {"input": [str(A)]}

if __name__ == "__main__":
    print(json.dumps([gen_case() for _ in range(20)]))
