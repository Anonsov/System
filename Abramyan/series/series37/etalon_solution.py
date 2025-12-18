k = int(input())
for _ in range(k):
    s = 0
    while True:
        x = int(input())
        if x == 0:
            break
        if x > 0:
            s += x
    print(s)
