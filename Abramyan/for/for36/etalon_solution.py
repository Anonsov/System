N = int(input().strip())
K = int(input().strip())
res = 0.0
for i in range(1, N+1):
    res += i ** K
print(res)
