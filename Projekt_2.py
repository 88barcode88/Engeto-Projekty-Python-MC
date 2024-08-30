"""
projekt_2.py: druhý projekt do Engeto Online Python Akademie
author: Miroslav Coufalík
email: mira.coufa@gmail.com
discord: 88barcode88
"""

import random

def pozdrav():
    print("Vítejte ve hře Bulls and Cows!")
    print("Vaším úkolem je uhádnout tajné 4místné číslo.")
    print("Číslice musí být unikátní a číslo nesmí začínat nulou.")
    print("Po každém pokusu vám řekneme, kolik máte 'bulls' a 'cows'.")
    print("1 bull = správné číslo na správném místě.")
    print("1 cow = správné číslo na nesprávném místě.")
    print("Pojďme začít!\n")

def generate_secret_number():
    digits = list('123456789')
    random.shuffle(digits)
    secret_number = digits.pop(0)
    digits += '0'
    random.shuffle(digits)
    secret_number += ''.join(digits[:3])
    return secret_number

def is_valid_guess(guess):
    if len(guess) != 4:
        return False, "Číslo musí mít přesně 4 číslice."
    if not guess.isdigit():
        return False, "Číslo může obsahovat pouze číslice."
    if guess[0] == '0':
        return False, "Číslo nesmí začínat nulou."
    if len(set(guess)) != 4:
        return False, "Číslo musí obsahovat unikátní číslice."
    return True, ""

def get_bulls_and_cows(secret, guess):
    bulls = sum(1 for s, g in zip(secret, guess) if s == g)
    cows = sum(1 for g in guess if g in secret) - bulls
    return bulls, cows

def play_game():
    pozdrav()
    secret_number = generate_secret_number()
    attempts = 0
    
    while True:
        guess = input("Zadejte svůj tip: ")
        valid, message = is_valid_guess(guess)
        if not valid:
            print(message)
            continue

        attempts += 1
        bulls, cows = get_bulls_and_cows(secret_number, guess)
        bulls_text = "bull" if bulls == 1 else "bulls"
        cows_text = "cow" if cows == 1 else "cows"
        print(f"{bulls} {bulls_text}, {cows} {cows_text}")

        if bulls == 4:
            print(f"Gratulujeme! Uhodli jste číslo {secret_number} v {attempts} pokusech.")
            break

if __name__ == "__main__":
    play_game()