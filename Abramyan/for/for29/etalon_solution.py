N = int(input().strip())
A = float(input().strip())
B = float(input().strip())
H = (B - A) / N
print(H)
for i in range(N+1):
    print(A + i*H)
