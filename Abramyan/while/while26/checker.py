def check(user_output: str, input_data: str) -> bool:
    n = int(input_data.strip())
    mx = 0
    while n > 0:
        d = n % 10
        if d > mx:
            mx = d
        n //= 10
    return user_output.strip() == str(mx)
