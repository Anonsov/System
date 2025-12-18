X = float(input().strip())
N = int(input().strip())
res = 1.0
p = 1.0
fact = 1.0
sign = -1.0
k = 0
for i in range(1, N+1):
    # next even term: power += 2, fact *= next two integers
    p *= X * X
    fact *= (2*k+1) * (2*k+2)
    k += 1
    res += sign * p / fact
    sign *= -1.0
print(res)
