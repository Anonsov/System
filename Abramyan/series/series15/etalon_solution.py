k = int(input())
idx = 0
pos = 0
while True:
    x = int(input())
    if x == 0:
        break
    idx += 1
    if pos == 0 and x > k:
        pos = idx
print(pos)
