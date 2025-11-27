n = int(input())
a = map(int, input().split())
target = int(input())
a = list(a)
n = len(a)


def binsss(a, target):
    l = 0
    r = n - 1
    while l <= r:
        m = (l + r) // 2
        if a[m] == target:
            return True
        elif a[m] < target:
            l = m + 1
        else:
            r = m - 1
    return False

print(binsss(a, target))