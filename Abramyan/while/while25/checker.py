def check(user_output: str, input_data: str) -> bool:
    n = int(input_data.strip())
    zeros = 0
    while n > 0:
        if n % 10 == 0:
            zeros += 1
        n //= 10
    return user_output.strip() == str(zeros)
