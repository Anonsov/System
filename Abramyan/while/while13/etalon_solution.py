A = float(input().strip())
S = 0.0
k = 0
i = 1
while S <= A:
    S += 1.0 / i
    k = i
    i += 1
print(k)
print(S)
