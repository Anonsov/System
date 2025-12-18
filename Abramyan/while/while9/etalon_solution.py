N = int(input().strip())
K = 0
p = 1
while p <= N:
    p *= 3
    K += 1
print(K)
