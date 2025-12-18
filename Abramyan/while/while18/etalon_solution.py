N = int(input().strip())
p = 1
while N > 0:
    p *= (N % 10)
    N //= 10
print(p)
