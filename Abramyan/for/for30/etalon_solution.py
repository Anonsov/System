import math
N = int(input().strip())
A = float(input().strip())
B = float(input().strip())
H = (B - A) / N
print(H)
for i in range(N+1):
    x = A + i*H
    print(1 - math.sin(x))
