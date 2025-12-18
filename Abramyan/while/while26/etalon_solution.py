N = int(input().strip())
mx = 0
while N > 0:
    d = N % 10
    if d > mx:
        mx = d
    N //= 10
print(mx)
