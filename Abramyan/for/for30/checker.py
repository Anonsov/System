import math

def check(user_output: str, expected_output: str) -> bool:
    try:
        u = float(user_output.strip())
        e = float(expected_output.strip())
    except Exception:
        return False
    return abs(u - e) <= 1e-6
