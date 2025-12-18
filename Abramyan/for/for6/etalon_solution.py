price = float(input().strip())
weights = [1.2 + 0.2*i for i in range(5)]  # 1.2,1.4,1.6,1.8,2.0
for w in weights:
    print(price * w)
