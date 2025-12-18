def check(user_output: str, input_data: str) -> bool:
    n = int(input_data.strip())
    all_odd = True
    if n == 0:
        all_odd = False
    while n > 0 and all_odd:
        if (n % 10) % 2 == 0:
            all_odd = False
            break
        n //= 10
    return user_output.strip() == str(all_odd)
