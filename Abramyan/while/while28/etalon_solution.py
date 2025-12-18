N = int(input().strip())
odd_count = 0
while N > 0:
    if (N % 10) % 2 == 1:
        odd_count += 1
    N //= 10
print(odd_count)
