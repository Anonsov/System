A = int(input().strip())
B = int(input().strip())
nums = list(range(B-1, A, -1))
print(len(nums))
for x in nums:
    print(x)
