N = int(input().strip())
count = 0
while N > 0:
    count += 1
    N //= 10
print(count)
