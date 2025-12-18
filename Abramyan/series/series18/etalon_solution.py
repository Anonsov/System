n = int(input())
prev = None
for _ in range(n):
    x = int(input())
    if prev is None or x != prev:
        print(x)
    prev = x
