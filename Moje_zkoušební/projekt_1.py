"""
projekt_1.py: první projekt do Engeto Online Python Akademie

author: Miroslav Coufalik
email: mira.coufa@gmail.com
discord: 88barcode88#1001
"""

import re

TEXTS = ['''
Situated about 10 miles west of Kemmerer,
Fossil Butte is a ruggedly impressive
topographic feature that rises sharply
some 1000 feet above Twin Creek Valley
to an elevation of more than 7500 feet
above sea level. The butte is located just
north of US 30N and the Union Pacific Railroad,
which traverse the valley. ''',
'''At the base of Fossil Butte are the bright
red, purple, yellow and gray beds of the Wasatch
Formation. Eroded portions of these horizontal
beds slope gradually upward from the valley floor
and steepen abruptly. Overlying them and extending
to the top of the butte are the much steeper
buff-to-white beds of the Green River Formation,
which are about 300 feet thick.''',
'''The monument contains 8198 acres and protects
a portion of the largest deposit of freshwater fish
fossils in the world. The richest fossil fish deposits
are found in multiple limestone layers, which lie some
100 feet below the top of the butte. The fossils
represent several varieties of perch, as well as
other freshwater genera and herring similar to those
in modern oceans. Other fish such as paddlefish,
garpike and stingray are also present.'''
]

users = {
    "bob": "123",
    "ann": "pass123",
    "mike": "password123",
    "liz": "pass123"
}

def get_user_credentials():
    username = input("username:")
    password = input("password:")
    return username, password

def authenticate_user(username, password):
    return users.get(username) == password

def select_text():
    while True:
        choice = input("Enter a number btw. 1 and 3 to select: ")
        if choice.isdigit() and 1 <= int(choice) <= 3:
            return TEXTS[int(choice) - 1]
        else:
            print("Invalid input. Terminating the program.")
            exit()

def analyze_text(text):
    words = re.findall(r'\b\w+\b', text)
    stats = {
        'total_words': len(words),
        'titlecase': sum(1 for word in words if word.istitle()),
        'uppercase': sum(1 for word in words if word.isupper()),
        'lowercase': sum(1 for word in words if word.islower()),
        'numeric': sum(1 for word in words if word.isdigit()),
        'sum_numeric': sum(int(word) for word in words if word.isdigit()),
        'word_lengths': {}
    }
    
    for word in words:
        length = len(word)
        stats['word_lengths'][length] = stats['word_lengths'].get(length, 0) + 1
    
    return stats

def display_results(stats):
    print("-" * 40)
    print(f"There are {stats['total_words']} words in the selected text.")
    print(f"There are {stats['titlecase']} titlecase words.")
    print(f"There are {stats['uppercase']} uppercase words.")
    print(f"There are {stats['lowercase']} lowercase words.")
    print(f"There are {stats['numeric']} numeric strings.")
    print(f"The sum of all the numbers {stats['sum_numeric']}")
    print("-" * 40)
    print("LEN|  OCCURRENCES  |NR.")
    print("-" * 40)
    
    for length in sorted(stats['word_lengths']):
        count = stats['word_lengths'][length]
        print(f"{length:3}|{'*' * count:15}|{count}")

def main():
    username, password = get_user_credentials()
    if authenticate_user(username, password):
        print("-" * 40)
        print(f"Welcome to the app, {username}")
        print("We have 3 texts to be analyzed.")
        print("-" * 40)
        selected_text = select_text()
        stats = analyze_text(selected_text)
        display_results(stats)
    else:
        print("unregistered user, terminating the program..")

if __name__ == "__main__":
    main()