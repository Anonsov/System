A = int(input().strip())
B = int(input().strip())
prod = 1.0
for x in range(A, B+1):
    prod *= x
print(prod)
