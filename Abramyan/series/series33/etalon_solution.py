k = int(input())
for _ in range(k):
    s = 0
    cnt = 0
    while True:
        x = int(input())
        if x == 0:
            break
        s += x
        cnt += 1
    print(s / cnt if cnt else 0)
