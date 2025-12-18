def check(user_output: str, expected_output: str) -> bool:
    ul = user_output.strip().splitlines()
    el = expected_output.strip().splitlines()
    if len(ul) != len(el):
        return False
    try:
        return all(abs(float(u) - float(e)) <= 1e-6 for u, e in zip(ul, el))
    except Exception:
        return False
