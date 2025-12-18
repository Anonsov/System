n = int(input())
idxs = []
for i in range(1, n + 1):
    x = int(input())
    if x % 2 != 0:
        idxs.append(i)

for i in idxs:
    print(i)
print(len(idxs))
