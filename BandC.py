import random

def generate_secret_number():
    digits = list('0123456789')
    random.shuffle(digits)
    return ''.join(digits[:4])

def get_bulls_and_cows(secret, guess):
    bulls = sum(1 for s, g in zip(secret, guess) if s == g)
    cows = sum(1 for g in guess if g in secret) - bulls
    return bulls, cows

def play_game():
    secret_number = generate_secret_number()
    attempts = 0
    while True:
        guess = input("Enter your guess: ")
        if len(guess) != 4 or not guess.isdigit():
            print("Invalid input. Please enter a 4-digit number.")
            continue
        attempts += 1
        bulls, cows = get_bulls_and_cows(secret_number, guess)
        print(f"Bulls: {bulls}, Cows: {cows}")
        if bulls == 4:
            print(f"Congratulations! You've guessed the number {secret_number} in {attempts} attempts.")
            break

if __name__ == "__main__":
    play_game()
