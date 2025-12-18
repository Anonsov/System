N = int(input().strip())
K = int(input().strip())
q = 0
r = N
if K > 0:
    while r >= K:
        r -= K
        q += 1
print(q)
print(r)
