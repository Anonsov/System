import math

n = int(input())
s_total = 0.0
for _ in range(n):
    x = float(input())
    ip = float(math.floor(x))
    s_total += ip
    # output as real number with .0
    if ip.is_integer():
        print(int(ip))
    else:
        print(ip)
print(s_total)
