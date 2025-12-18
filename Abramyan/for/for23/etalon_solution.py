X = float(input().strip())
N = int(input().strip())
res = 0.0
p = X
fact = 1.0
sign = 1.0
k = 1
for i in range(N):
    if i > 0:
        # move from k to next odd exponent
        p *= X * X  # power increases by 2
        fact *= (k+1) * (k+2)
        k += 2
        sign *= -1.0
    res += sign * p / fact
print(res)
