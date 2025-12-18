N = int(input().strip())
a1, a2, a3 = 1, 2, 3
print(a1)
if N >= 2:
    print(a2)
if N >= 3:
    print(a3)
for _ in range(4, N+1):
    a1, a2, a3 = a2, a3, a3 + a2 - 2*a1
    print(a3)
