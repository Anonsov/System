A = int(input().strip())
B = int(input().strip())
for i, k in enumerate(range(A, B+1), start=1):
    for _ in range(i):
        print(k)
