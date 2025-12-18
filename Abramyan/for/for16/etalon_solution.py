A = float(input().strip())
N = int(input().strip())
cur = 1.0
for _ in range(N):
    cur *= A
    print(cur)
