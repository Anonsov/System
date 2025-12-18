N = int(input().strip())
# Largest Fibonacci number <= N and its index (F1=1, F2=1,...)
if N == 1:
    print(1)
    print(1)
else:
    f0, f1 = 1, 1
    idx = 2  # f1 index
    last_val, last_idx = 1, 1
    while f1 <= N:
        last_val, last_idx = f1, idx
        f0, f1 = f1, f0 + f1
        idx += 1
    print(last_idx)
    print(last_val)
