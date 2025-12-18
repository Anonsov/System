n = int(input())
prev = int(input())
res = []
for _ in range(n - 1):
    x = int(input())
    if x < prev:
        res.append(x)
    prev = x
for x in res:
    print(x)
print(len(res))
