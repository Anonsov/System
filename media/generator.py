import random

# print(res)

def generate_input():
    lo_len = 1
    hi_len = 2 * (10**5)
    lo_num = 1
    hi_num = 2 * (10**9)
    n = random.randint(lo_len, hi_len)
    res = []
    for i in range(n):
        res.append(random.randint(lo_num, hi_num))
    return res
