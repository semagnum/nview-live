def format_round(num, division_amount: float):
    return str(int(round(num / division_amount, 1)))


def format_num(num):
    if num < 1000:
        return str(num)
    elif num < 1000000:
        return format_round(num, 1000.0) + 'k'
    elif num < 1000000000:
        return format_round(num, 1000000.0) + 'M'
    return format_round(num, 1000000000.0) + 'B'
