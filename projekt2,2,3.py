# Seznam zadaných slov
zadana_slova = ["Matous", "Martin", "ahoj", "sos", "er", "es", "i", "a"]

# Vyberme libovolné slovo z listu pomocí indexu
index = 3  # Například zvolíme index 0 pro první slovo
slovo = zadana_slova[index]

# Zjistíme délku vybraného slova a uložíme ji do proměnné delka_slova
delka_slova = len(slovo)

# Kontrola podmínek a výpis výsledku
if delka_slova >= 4:
    print(f"{slovo} počet znaků: {delka_slova}")
elif 2 <= delka_slova <= 3:
    print(f"{slovo} počet znaků: {delka_slova}")
elif delka_slova == 1:
    print(f"{slovo} počet znaků {delka_slova}")