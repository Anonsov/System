N = int(input().strip())
zeros = 0
while N > 0:
    if N % 10 == 0:
        zeros += 1
    N //= 10
print(zeros)
