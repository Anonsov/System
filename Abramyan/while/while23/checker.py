def check(user_output: str, input_data: str) -> bool:
    n = int(input_data.strip())
    all_even = True
    if n == 0:
        all_even = True
    while n > 0:
        if (n % 10) % 2 == 1:
            all_even = False
            break
        n //= 10
    return user_output.strip() == str(all_even)
