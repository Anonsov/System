def check(user_output: str, input_data: str) -> bool:
    n = int(input_data.strip())
    odd_count = 0
    while n > 0:
        if (n % 10) % 2 == 1:
            odd_count += 1
        n //= 10
    return user_output.strip() == str(odd_count)
