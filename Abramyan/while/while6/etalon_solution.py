N = int(input().strip())
res = 1.0
k = N if N % 2 == 1 else N
while k >= 1:
    res *= k
    k -= 2
print(res)
