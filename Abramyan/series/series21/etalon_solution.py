n = int(input())
prev = float(input())
ok = True
for _ in range(n - 1):
    x = float(input())
    if x < prev:
        ok = False
    prev = x
print("True" if ok else "False")
