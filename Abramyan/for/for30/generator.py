import json, random, math
if __name__ == "__main__":
    def gen():
        N = random.randint(2, 50)
        A = round(random.uniform(-math.pi, math.pi), 6)
        B = round(random.uniform(A+0.001, min(A+2*math.pi, math.pi)), 6)
        return {"input": [str(N), str(A), str(B)]}
    print(json.dumps([gen() for _ in range(20)]))
