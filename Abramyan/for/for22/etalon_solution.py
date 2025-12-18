X = float(input().strip())
N = int(input().strip())
res = 1.0
p = 1.0
fact = 1.0
for k in range(1, N+1):
    p *= X
    fact *= k
    res += p / fact
print(res)
