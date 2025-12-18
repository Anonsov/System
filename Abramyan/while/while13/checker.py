def check(user_output: str, expected_output: str) -> bool:
    ul = user_output.strip().splitlines()
    el = expected_output.strip().splitlines()
    if len(ul) != 2 or len(el) != 2:
        return False
    if ul[0].strip() != el[0].strip():
        return False
    try:
        u2 = float(ul[1].strip()); e2 = float(el[1].strip())
    except Exception:
        return False
    return abs(u2 - e2) <= 1e-6
