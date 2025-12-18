N = int(input().strip())
a1 = 1.0
a2 = 2.0
print(a1)
if N >= 2:
    print(a2)
for _ in range(3, N+1):
    a1, a2 = a2, (a1 + 2*a2) / 3.0
    print(a2)
