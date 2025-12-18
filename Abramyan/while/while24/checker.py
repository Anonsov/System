def check(user_output: str, input_data: str) -> bool:
    orig = int(input_data.strip())
    n = orig
    rev = 0
    while n > 0:
        rev = rev * 10 + (n % 10)
        n //= 10
    return user_output.strip() == str(orig == rev)
