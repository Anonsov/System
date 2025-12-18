# Interpreting series (from problem text) as alternating with odd factorial denominators times rising products (double factorial style).
X = float(input().strip())
N = int(input().strip())
# Using Taylor for sin with a coefficient accumulator akin to given form
res = 0.0
p = X
fact = 1.0
sign = 1.0
k = 1
for i in range(N):
    if i > 0:
        p *= X * X
        fact *= (k+1) * (k+2)
        k += 2
        sign *= -1.0
    res += sign * p / fact
print(res)
