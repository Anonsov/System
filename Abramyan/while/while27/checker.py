def check(user_output: str, input_data: str) -> bool:
    n = int(input_data.strip())
    mn = 9
    while n > 0:
        d = n % 10
        if d < mn:
            mn = d
        n //= 10
    return user_output.strip() == str(mn)
