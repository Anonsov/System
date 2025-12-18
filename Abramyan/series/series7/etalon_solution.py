import math

n = int(input())
s = 0
for _ in range(n):
    x = float(input())
    # round to nearest integer: for .5 cases use standard rounding away from zero
    if x >= 0:
        r = int(math.floor(x + 0.5))
    else:
        r = int(math.ceil(x - 0.5))
    print(r)
    s += r
print(s)
