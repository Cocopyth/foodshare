from emoji import emojize


def emojize_number(number):
    return ''.join(emojize(f':keycap_{digit}:') for digit in str(number))
