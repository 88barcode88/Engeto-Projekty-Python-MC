# Zadané proměnné
user_email = {"email": "marek.parek@gmail.com"}

# Vytvoř nový slovník "user_1"
user_1 = {}

# Doplň klíče "name" a "surname" s hodnotami "Marek" a "Parek"
user_1["name"] = "Marek"
user_1["surname"] = "Parek"

# Doplň slovník "user_1" o slovník "user_email"
user_1.update(user_email)

# Vypiš hodnoty ze slovníku "user_1" s doplňujícím textem
print(f"User #01: {user_1}")