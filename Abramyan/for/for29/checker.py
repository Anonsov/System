def check(user_output: str, expected_output: str) -> bool:
    return user_output.strip().splitlines() == expected_output.strip().splitlines()
