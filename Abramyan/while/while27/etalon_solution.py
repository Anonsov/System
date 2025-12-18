N = int(input().strip())
mn = 9
while N > 0:
    d = N % 10
    if d < mn:
        mn = d
    N //= 10
print(mn)
