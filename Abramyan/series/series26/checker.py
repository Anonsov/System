from Abramyan.series._common_checker import check_float_lines


def check(user_output: str, expected_output: str) -> bool:
    return check_float_lines(user_output, expected_output, tol=1e-6)
