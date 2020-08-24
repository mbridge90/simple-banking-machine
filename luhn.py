import random


def get_luhn_total(number_to_check):
    number_for_algorithm = str(number_to_check)[:15]
    sequence = [int(num) for num in list(number_for_algorithm)]

    i = 0
    while i < len(number_for_algorithm):
        sequence[i] = sequence[i] * 2
        i += 2

    j = 0
    while j < len(sequence):
        if sequence[j] > 9:
            sequence[j] = sequence[j] - 9
        j += 1

    total = 0
    for number in sequence:
        total += number

    return total


def check_card_number(number_to_check):
    checksum = int(number_to_check[-1])

    total = get_luhn_total(number_to_check)

    return 10 - (total % 10) == checksum


def generate_card_number():
    initial_card_number = '400000' + str((random.randint(0, 999999999))).zfill(9)

    total = get_luhn_total(initial_card_number)

    checksum = 0
    if total % 10 != 0:
        checksum = 10 - (total % 10)

    return initial_card_number + str(checksum)
