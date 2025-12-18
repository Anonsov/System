from Abramyan.series._common_checker import check_text


def check(user_output: str, expected_output: str) -> bool:
    return check_text(user_output, expected_output)
