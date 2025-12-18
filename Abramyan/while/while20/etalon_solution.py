N = int(input().strip())
has_odd = False
while N > 0:
    if (N % 10) % 2 == 1:
        has_odd = True
        break
    N //= 10
print(has_odd)
