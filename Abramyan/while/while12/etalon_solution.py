N = int(input().strip())
# Smallest Fibonacci number > N and its index (F1=1, F2=1,...)
if N < 1:
    print(1)
    print(1)
else:
    f0, f1 = 1, 1
    idx = 2
    while f1 <= N:
        f0, f1 = f1, f0 + f1
        idx += 1
    print(idx)
    print(f1)
