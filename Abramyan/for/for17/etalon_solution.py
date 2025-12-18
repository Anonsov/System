A = float(input().strip())
N = int(input().strip())
res = 1.0
p = 1.0
for _ in range(N):
    p *= A
    res += p
print(res)
