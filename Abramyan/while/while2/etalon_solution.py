A = float(input().strip())
B = float(input().strip())
count = 0
if B > 0:
    eps = 1e-12
    while A + eps >= B:
        A -= B
        count += 1
print(count)
