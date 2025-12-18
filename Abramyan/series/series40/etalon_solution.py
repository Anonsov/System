k = int(input())
for _ in range(k):
    cnt = 0
    s = 0
    while True:
        x = int(input())
        if x == 0:
            break
        cnt += 1
        s += x
    print(s / cnt if cnt else 0)
