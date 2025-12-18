N = int(input().strip())
all_odd = True
if N == 0:
    all_odd = False
while N > 0 and all_odd:
    if (N % 10) % 2 == 0:
        all_odd = False
        break
    N //= 10
print(all_odd)
