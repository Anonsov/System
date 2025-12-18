N = int(input().strip())
res = 1.0
fact = 1.0
for k in range(1, N+1):
    fact *= k
    res += 1.0 / fact
print(res)
