N = int(input().strip())
all_even = True
if N == 0:
    all_even = True
while N > 0:
    if (N % 10) % 2 == 1:
        all_even = False
        break
    N //= 10
print(all_even)
