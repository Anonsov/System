N = int(input().strip())
if N >= 1:
    print(1)
if N >= 2:
    print(1)
a, b = 1, 1
for _ in range(3, N+1):
    a, b = b, a + b
    print(b)
