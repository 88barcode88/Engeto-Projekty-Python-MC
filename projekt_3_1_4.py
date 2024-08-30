jmeno = 'Marek'
heslo = '1234'
uzivatel = {'Marek': '1234'}

if jmeno in uzivatel and uzivatel[jmeno] == heslo:
    print("Ahoj", jmeno, "vítej v aplikaci! Pokračuj...")
else:
    print("Uživatelské jméno nebo heslo nejsou v pořádku!")




