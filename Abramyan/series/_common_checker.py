def _split_lines(s: str) -> list[str]:
    s = s.strip()
    return [] if not s else s.splitlines()


def check_float_lines(user_output: str, expected_output: str, tol: float = 1e-6) -> bool:
    ul = _split_lines(user_output)
    el = _split_lines(expected_output)
    if len(ul) != len(el):
        return False
    try:
        return all(abs(float(u) - float(e)) <= tol for u, e in zip(ul, el))
    except Exception:
        return False


def check_text(user_output: str, expected_output: str) -> bool:
    return user_output.strip() == expected_output.strip()
