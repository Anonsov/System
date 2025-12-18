def check(user_output: str, input_data: str) -> bool:
    n = int(input_data.strip())
    has_even = False
    while n > 0:
        if (n % 10) % 2 == 0:
            has_even = True
            break
        n //= 10
    return user_output.strip() == str(has_even)
