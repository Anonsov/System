N = int(input().strip())
s = 0
odd = 1
for _ in range(N):
    s += odd
    print(s)
    odd += 2
