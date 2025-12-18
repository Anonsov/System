N = int(input().strip())
res = 0.0
sign = 1.0
x = 1.1
for _ in range(N):
    res += sign * x
    sign *= -1.0
    x += 0.1
print(res)
