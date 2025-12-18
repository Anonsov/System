A = float(input().strip())
S = 0.0
i = 1
while True:
    term = 1.0 / i
    if S + term > A:
        break
    S += term
    i += 1
k = i - 1
print(k)
print(S)
