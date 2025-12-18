N = int(input().strip())
prod = 1.0
x = 1.1
for _ in range(N):
    prod *= x
    x += 0.1
print(prod)
