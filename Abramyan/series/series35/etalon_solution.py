k = int(input())
for _ in range(k):
    mn = None
    while True:
        x = int(input())
        if x == 0:
            break
        if mn is None or x < mn:
            mn = x
    print(mn if mn is not None else 0)
