k = int(input())
ns = [int(input()) for _ in range(k)]
for n in ns:
    s = 0
    for _ in range(n):
        s += int(input())
    print(s)
