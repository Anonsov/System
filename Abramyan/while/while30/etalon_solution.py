A = int(input().strip())
B = int(input().strip())
# GCD using subtraction-based Euclidean algorithm
while A != B:
    if A > B:
        A -= B
    else:
        B -= A
print(A)
