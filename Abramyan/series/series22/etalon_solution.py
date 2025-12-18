n = int(input())
prev = float(input())
# descending means prev >= next >= ...
for i in range(2, n + 1):
    x = float(input())
    if x > prev:
        print(i)
        break
    prev = x
else:
    print(0)
