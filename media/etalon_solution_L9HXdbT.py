x = float(input().strip())

def sqrt_bin_search(x):
    if x == 0:
        return 0.0

    l, r = 0.0, max(1.0, x)
    eps = 1e-6

    while r - l > eps:
        m = (l + r) / 2
        if m * m > x:
            r = m
        else:
            l = m

    return (l + r) / 2

ans = sqrt_bin_search(x)

print(f"{ans:.6f}")
