n = int(input())
k = 0
for _ in range(n):
    x = int(input())
    if x % 2 == 0:
        print(x)
        k += 1
print(k)
