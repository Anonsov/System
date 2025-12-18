k = int(input())
n = int(input())
ok = True
for _ in range(n):
    if int(input()) < k:
        ok = False
print("True" if ok else "False")
