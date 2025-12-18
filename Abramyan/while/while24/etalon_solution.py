N = int(input().strip())
orig = N
rev = 0
while N > 0:
    rev = rev * 10 + (N % 10)
    N //= 10
print(orig == rev)
