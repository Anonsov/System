def check(user_output: str, input_data: str) -> bool:
    a_s, b_s = input_data.strip().split()
    a = int(a_s); b = int(b_s)
    # GCD via subtraction
    x, y = a, b
    while x != y:
        if x > y:
            x -= y
        else:
            y -= x
    return user_output.strip() == str(x)
