k = int(input())
cnt = 0
while True:
    x = int(input())
    if x == 0:
        break
    if x < k:
        cnt += 1
print(cnt)
