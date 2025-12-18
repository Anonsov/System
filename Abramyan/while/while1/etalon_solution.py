A = float(input().strip())
B = float(input().strip())
# remainder of A by B using subtraction
if B <= 0:
    print(A)
else:
    eps = 1e-12
    while A + eps >= B:
        A -= B
    print(A)
