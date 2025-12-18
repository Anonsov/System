N = int(input().strip())
res = 0.0
fact = 1.0
for k in range(1, N+1):
    fact *= k
    res += fact
print(res)
