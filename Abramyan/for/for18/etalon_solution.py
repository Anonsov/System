A = float(input().strip())
N = int(input().strip())
res = 1.0
p = 1.0
sign = -1.0
for k in range(1, N+1):
    p *= A
    res += sign * p
    sign *= -1.0
print(res)
