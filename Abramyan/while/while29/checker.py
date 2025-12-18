def check(user_output: str, input_data: str) -> bool:
    n = int(input_data.strip())
    even_count = 0
    while n > 0:
        if (n % 10) % 2 == 0:
            even_count += 1
        n //= 10
    return user_output.strip() == str(even_count)
