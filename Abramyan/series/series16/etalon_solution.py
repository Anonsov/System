k = int(input())
idx = 0
last = 0
while True:
    x = int(input())
    if x == 0:
        break
    idx += 1
    if x > k:
        last = idx
print(last)
