# Seznam čísel
vstupni_cisla = [1, 2, 3, 4, 5, 6, 7]

# Seznam písmen odpovídajících dnům v týdnu
vstupni_pismena = ["p", "ú", "s", "č", "p", "s", "n"]

# Týdenní dny
tyden = ('pondělí', 'úterý', 'středa', 'čtvrtek', 'pátek', 'sobota', 'neděle')

# Získání vstupu od uživatele
cislo_dne = int(input("Zadejte číslo dne: "))

# Kontrola, zda je cislo_dne v seznamu vstupni_cisla
if cislo_dne in vstupni_cisla:
    # Indexování seznamu tyden (0-based index)
    den_tydne = tyden[cislo_dne - 1]
    print("Správná vstupní hodnota")
    print(f'Den týdne odpovídající číslu {cislo_dne} je {den_tydne}.')

    # Ověření, zda první písmeno dne týdne odpovídá písmenu v seznamu vstupni_pismena
    if den_tydne[0] == vstupni_pismena[cislo_dne - 1]:
        print(f"První písmeno dne '{den_tydne}' odpovídá písmenu '{vstupni_pismena[cislo_dne - 1]}' v seznamu vstupni_pismena.")
    else:
        print(f"První písmeno dne '{den_tydne}' NEodpovídá písmenu '{vstupni_pismena[cislo_dne - 1]}' v seznamu vstupni_pismena.")
elif cislo_dne not in vstupni_cisla:
    print("Špatná vstupní hodnota!")