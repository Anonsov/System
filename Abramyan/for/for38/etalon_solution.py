N = int(input().strip())
res = 0.0
p = 1.0
for i in range(1, N+1):
    p *= i
    res += (i ** (N - i + 1))
print(res)
