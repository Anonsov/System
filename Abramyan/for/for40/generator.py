import json, random
if __name__ == "__main__":
    def gen():
        A = random.randint(1, 20)
        B = random.randint(A+1, A+20)
        return {"input": [str(A), str(B)]}
    print(json.dumps([gen() for _ in range(20)]))
