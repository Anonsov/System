import json, random

def gen_case():
    E = 10 ** (-random.randint(1, 6))
    return {"input": [str(E)]}

if __name__ == "__main__":
    print(json.dumps([gen_case() for _ in range(20)]))
