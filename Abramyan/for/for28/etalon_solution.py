# Binomial series for sqrt(1+X)
X = float(input().strip())
N = int(input().strip())
res = 1.0
coef = 1.0
p = 1.0
for k in range(1, N+1):
    coef *= (0.5 - (k-1)) / k
    p *= X
    res += coef * p
print(res)
