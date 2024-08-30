"""
projekt_2.py: druhý projekt do Engeto Online Python Akademie

author: Miroslav Coufalik
email: mira.coufa@gmail.com
discord: 88barcode88#1001
"""

import random
import time

def generate_secret_number():
    digits = list(range(10))  
    random.shuffle(digits)
    if digits[0] == 0:  
        digits[0], digits[1] = digits[1], digits[0]
    return ''.join(map(str, digits[:4]))

def validate_guess(guess):
    if not guess.isdigit():
        return False, "Please enter only numeric digits."
    if len(guess) != 4:
        return False, "Please enter exactly 4 digits."
    if guess[0] == '0':
        return False, "The number cannot start with zero."
    if len(set(guess)) != 4:
        return False, "The digits must be unique."
    return True, ""

def evaluate_guess(secret, guess):
    bulls = sum(s == g for s, g in zip(secret, guess))
    cows = sum(g in secret for g in guess) - bulls
    return bulls, cows

def format_result(bulls, cows):
    bull_str = f"{bulls} bull{'s' if bulls != 1 else ''}"
    cow_str = f"{cows} cow{'s' if cows != 1 else ''}"
    return f"{bull_str}, {cow_str}"

def rate_performance(guesses):
    if guesses <= 5:
        return "amazing"
    elif guesses <= 10:
        return "good"
    elif guesses <= 15:
        return "average"
    else:
        return "not so good"

def play_game():
    print("Hi there!")
    print("-" * 47)
    print("I've generated a random 4 digit number for you.")
    print("Let's play a bulls and cows game.")
    print("-" * 47)
    
    secret = generate_secret_number()
    guesses = 0
    start_time = time.time()
    
    while True:
        print("Enter a number:")
        print("-" * 47)
        guess = input(">>> ")
        valid, message = validate_guess(guess)
        if not valid:
            print(message)
            print("-" * 47)
            continue
        
        guesses += 1
        bulls, cows = evaluate_guess(secret, guess)
        
        if bulls == 4:
            end_time = time.time()
            time_taken = round(end_time - start_time, 2)
            print(f"Correct, you've guessed the right number")
            print(f"in {guesses} guesses!")
            print("-" * 47)
            print(f"It took you {time_taken} seconds.")
            print(f"That's {rate_performance(guesses)}!")
            break
        else:
            print(format_result(bulls, cows))
            print("-" * 47)

if __name__ == "__main__":
    play_game()