X = float(input().strip())
N = int(input().strip())
res = 0.0
p = X
sign = 1.0
for k in range(1, N+1):
    if k > 1:
        p *= X * X
    res += sign * p / (2*k - 1)
    sign *= -1.0
print(res)
