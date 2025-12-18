n = int(input())
arr0 = int(input())
prev = arr0
res = []
# we need compare each element with its right neighbor
# read next, decide for prev
for _ in range(n - 1):
    nxt = int(input())
    if prev < nxt:
        res.append(prev)
    prev = nxt
for x in res:
    print(x)
print(len(res))
