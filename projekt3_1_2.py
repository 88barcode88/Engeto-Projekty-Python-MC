# Zadaný nestovaný slovník
employees = {
    'employee01': {
        'name': 'Marek',
        'surname': 'Parek',
        'email': 'marek.parek@gmail.com'
    },
    'employee02': {
        'name': 'Matous',
        'surname': 'Svatous',
        'email': 'matous.svatous@gmail.com'
    },
    'employee03': {
        'name': 'anna',
        'surname': 'rana',
        'email': 'anna.rana@gmail.com'
    }
}
# Nejprve vypiš všechny klíče ze slovníku "employees" s doplňujícím oznámením
print("Všechny klíče¨: ", employees.keys())
# Vypiš všechny hodnoty ze slovníku "employees" s doplňujícím oznámením
print("Všechny hodnoty: ", employees.values())
# Vypiš jak hodnoty, tak klíče zaměstnance "employee03"
print("Všechny údaje k poslednímu zaměstnanci: ", employees['employee03'].items())