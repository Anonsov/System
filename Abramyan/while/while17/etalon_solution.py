N = int(input().strip())
s = 0
while N > 0:
    s += N % 10
    N //= 10
print(s)
