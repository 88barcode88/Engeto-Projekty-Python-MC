vysledek = []
zadana_cisla = '1,2,3,4,5'
cisla = zadana_cisla.split(',')
for item in cisla:
    vysledek.append(int(item.strip()))
print(f"List: {vysledek}")
