n = int(input())
s = 0.0
p = 1.0
for _ in range(n):
    x = float(input())
    s += x
    p *= x
print(s)
print(p)
