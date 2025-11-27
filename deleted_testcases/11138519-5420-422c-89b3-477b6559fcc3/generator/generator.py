import random

def small_tests():
    tests = []
    # 1
    tests.append((1, [5], 5))
    
    # 2
    tests.append((5, [1,2,3,4,5], 3))
    
    # 3 target not found
    tests.append((5, [1,2,3,4,5], 10))
    
    return tests

def medium_tests():
    tests = []
    for _ in range(5):
        n = random.randint(50, 500)
        arr = sorted(random.randint(1, 10000) for _ in range(n))
        target = random.randint(1, 10000)
        tests.append((n, arr, target))
    return tests

def large_tests():
    tests = []
    for _ in range(3):
        n = 200000
        arr = sorted(random.randint(1, 2_000_000_000) for _ in range(n))
        target = random.randint(1, 2_000_000_000)
        tests.append((n, arr, target))
    return tests

def edge_tests():
    tests = []
    # target smaller than all
    n = 100000
    arr = sorted(random.randint(10, 10000000) for _ in range(n))
    tests.append((n, arr, 1))
    
    # all equal
    arr = [42] * 200000
    tests.append((200000, arr, 42))
    
    tests.append((200000, arr, 100))
    return tests

def random_tests():
    tests = []
    for _ in range(3):
        n = random.randint(1, 200000)
        arr = sorted(random.randint(1, 10**9) for _ in range(n))
        target = random.randint(1, 10**9)
        tests.append((n, arr, target))
    return tests


def generate_all_tests():
    tests = []
    tests += small_tests()
    tests += medium_tests()
    tests += large_tests()
    tests += edge_tests()
    tests += random_tests()
    return len(tests)

print(generate_all_tests())