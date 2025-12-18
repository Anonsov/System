E = float(input().strip())
# Smallest n such that 1/n <= E
n = 1
while 1.0 / n > E:
    n += 1
print(n)
