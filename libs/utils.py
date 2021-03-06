from random import randint


def str2bool(value):
    """
    convert string to bool
    """
    if value:
        return value.lower() in ("true",)
    else:
        return False


def get_verification_code():
    return randint(100000, 999999)


def get_random_int():
    return randint(100000, 999999)


def get_random_between_given(start, end):
    return randint(start, end)
