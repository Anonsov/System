import json, random

def gen_case():
    # Keep loops small: K in [1, 10000], N in [0, K*1000]
    K = random.randint(1, 10000)
    N = random.randint(0, K * 1000)
    return {"input": [str(N), str(K)]}

if __name__ == "__main__":
    print(json.dumps([gen_case() for _ in range(20)]))
