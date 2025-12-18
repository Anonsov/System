n = int(input())
arr = [int(input()) for _ in range(n)]
# indices of zeros
zeros = [i for i, x in enumerate(arr) if x == 0]
# sum between last two zeros
z1, z2 = zeros[-2], zeros[-1]
if z2 - z1 <= 1:
    print(0)
else:
    print(sum(arr[z1 + 1 : z2]))
