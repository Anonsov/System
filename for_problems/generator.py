# generator_test.py
import random
import json

def small_tests():
    return [
        0.0,
        1.0,
        4.0,
        0.25,
        100.0
    ]

def medium_tests():
    tests = []
    for _ in range(5):
        x = random.uniform(0, 1e6)
        tests.append(x)
    return tests

def large_tests():
    tests = []
    for _ in range(3):
        x = random.uniform(0, 1e18)
        tests.append(x)
    return tests

def edge_tests():
    return [
        1e-12,      
        1e18,      
        1e-9,       
        999999999999.0
    ]

def random_tests():
    tests = []
    for _ in range(5):
        x = random.random() * random.randint(1, 10**12)
        tests.append(x)
    return tests

def generate_all():
    numbers = []
    numbers += small_tests()
    numbers += medium_tests()
    numbers += large_tests()
    numbers += edge_tests()
    numbers += random_tests()

    tests = []
    for x in numbers:
        tests.append({
            "input": [str(x)]
        })

    return tests

if __name__ == "__main__":
    print(json.dumps(generate_all()))
