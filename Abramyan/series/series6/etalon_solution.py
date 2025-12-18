import math

n = int(input())
prod = 1.0
for _ in range(n):
    x = float(input())
    frac = x - math.floor(x)
    prod *= frac
    print(frac)
print(prod)
