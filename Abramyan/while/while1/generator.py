import json, random

def gen_case():
    b = round(random.uniform(0.1, 100.0), 6)
    a = round(b + random.uniform(0.01, 500.0), 6)
    return {"input": [str(a), str(b)]}

if __name__ == "__main__":
    print(json.dumps([gen_case() for _ in range(20)]))
