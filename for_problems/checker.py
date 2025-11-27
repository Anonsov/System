def check(user_output: str, input_data: str) -> bool:
    x = float(input_data.strip())
    try:
        y = float(user_output.strip()) 
    except ValueError:
        return False
    
    e = 1e-6
    return abs(y - x) <= e
