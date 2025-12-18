n = int(input())
if n <= 2:
    print(0)
    raise SystemExit

prev = float(input())
cur = float(input())
# check each inner element (2..n-1)
for idx in range(2, n):
    nxt = float(input())
    if not ((cur > prev and cur > nxt) or (cur < prev and cur < nxt)):
        print(idx)
        break
    prev, cur = cur, nxt
else:
    print(0)
