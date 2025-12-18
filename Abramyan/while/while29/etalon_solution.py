N = int(input().strip())
even_count = 0
while N > 0:
    if (N % 10) % 2 == 0:
        even_count += 1
    N //= 10
print(even_count)
