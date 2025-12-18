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
    if cnt == 0:
        print(0)
    else:
        print(s / cnt)
        # if 0 terminator should not count, already excluded
