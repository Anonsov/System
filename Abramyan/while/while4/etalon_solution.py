N = int(input().strip())
if N <= 0:
    print(False)
else:
    while N % 3 == 0:
        N //= 3
    print(N == 1)
