N = int(input().strip())
has_even = False
while N > 0:
    if (N % 10) % 2 == 0:
        has_even = True
        break
    N //= 10
print(has_even)
