cisla = [1, 2, 3, 4, 5, 6, 7, 8]
suda = 0
licha = 0
for cislo in cisla:
    if cislo % 2 == 0:
        suda += cislo
    else:
        licha += cislo
rozdil = licha - suda
vysledek = abs(rozdil)
print(f"Rozdíl je: {vysledek}")