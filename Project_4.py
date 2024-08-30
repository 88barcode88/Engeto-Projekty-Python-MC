jmeno = "Martin"
vaha = 80
vyska = 200 / 100
bmi = vaha / vyska ** 2
if bmi > 40:
    kategorie = 'těžká obezita'
elif bmi > 30:
    kategorie = 'obezita'
elif bmi > 25:
    kategorie = 'mírná nadváha'
elif bmi > 18.5:
    kategorie = 'zdravá váha'
else:
    kategorie = 'podvýživa'

print(jmeno, "tvé BMI je", bmi, "což spadá do kategorie", kategorie, ".")