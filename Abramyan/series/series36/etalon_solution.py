k = int(input())
for _ in range(k):
    mx = None
    while True:
        x = int(input())
        if x == 0:
            break
        if mx is None or x > mx:
            mx = x
    print(mx if mx is not None else 0)
