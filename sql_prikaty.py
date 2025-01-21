from reportlab.lib.pagesizes import letter, landscape
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import os

# Cesta k fontu DejaVuSans.ttf
# Ujistěte se, že máte tento font ve stejné složce jako váš skript nebo zadejte správnou cestu
font_path = "DejaVuSans.ttf"

if not os.path.exists(font_path):
    raise FileNotFoundError(f"Fontový soubor '{font_path}' nebyl nalezen. Prosím, ujistěte se, že je na správné cestě.")

# Registrace fontu
pdfmetrics.registerFont(TTFont('DejaVu', font_path))

# Definice stylů
styles = getSampleStyleSheet()
styleN = ParagraphStyle(
    'Normal',
    parent=styles['Normal'],
    fontName='DejaVu',
    fontSize=9,  # Mírně menší font pro lepší přizpůsobení
    leading=11,
)
styleH = ParagraphStyle(
    'Header',
    parent=styles['Heading4'],
    fontName='DejaVu',
    fontSize=10,  # Mírně menší font pro hlavičku
    leading=12,
    alignment=1,  # Center alignment
    textColor=colors.whitesmoke,
)

# Data z dokumentu s použitím Paragraph pro správné zalamování textu
data = [
    [Paragraph("Název příkazu", styleH), 
     Paragraph("Popis", styleH), 
     Paragraph("Příklad", styleH)],
    ["AS", "Aliasy pro přejmenování sloupců nebo tabulek.", "SELECT name AS employee_name FROM employees;"],
    ["AVG()", "Agregační funkce pro výpočet průměrné hodnoty.", "SELECT AVG(salary) FROM employees;"],
    ["SUM()", "Agregační funkce pro součet hodnot ve sloupci.", "SELECT SUM(salary) FROM employees;"],
    ["MIN()", "Vrací minimální hodnotu ve sloupci.", "SELECT MIN(salary) FROM employees;"],
    ["MAX()", "Vrací maximální hodnotu ve sloupci.", "SELECT MAX(salary) FROM employees;"],
    ["MEDIAN()", "Vrací medián hodnot ve sloupci.", "SELECT MEDIAN(salary) FROM employees;"],
    ["STDDEV()", "Výpočet směrodatné odchylky ve sloupci.", "SELECT STDDEV(salary) FROM employees;"],
    ["VARIANCE()", "Výpočet rozptylu hodnot ve sloupci.", "SELECT VARIANCE(salary) FROM employees;"],
    ["PERCENTILE_COUNT()", "Vrací procentní počet hodnot ve sloupci, což reprezentuje hodnotu, která odpovídá specifikovanému percentilu.", "SELECT PERCENTILE_COUNT(0.9) WITHIN GROUP (ORDER BY salary) FROM employees;"],
    ["PERCENTILE_DISC()", "Vrací diskrétní procentil hodnot ve sloupci, což reprezentuje hodnotu, která odpovídá specifikovanému percentilu.", "SELECT PERCENTILE_DISC(0.5) WITHIN GROUP (ORDER BY salary) FROM employees;"],
    ["Agregační funkce", "Funkce pro výpočty jako SUM(), AVG(), MIN(), MAX(), MEDIAN(), STDDEV(), VARIANCE(), PERCENTILE_COUNT(), PERCENTILE_DISC().", "SELECT SUM(salary) FROM employees;"],
    ["CASE", "Podmínkový příkaz pro přiřazení hodnot podle splněných podmínek.", "SELECT name, CASE WHEN age > 30 THEN 'Senior' ELSE 'Junior' END AS category FROM employees;"],
    ["COUNT(DISTINCT)", "Počítá počet unikátních hodnot ve sloupci.", "SELECT COUNT(DISTINCT department) FROM employees;"],
    ["COUNT()", "Počítá počet řádků nebo hodnot ve sloupci.", "SELECT COUNT(*) FROM employees;"],
    ["CREATE OR REPLACE VIEW", "Vytvoří nebo nahradí existující pohled (view).", "CREATE OR REPLACE VIEW emp_view AS SELECT * FROM employees;"],
    ["DROP VIEW", "Odstraní existující pohled (view).", "DROP VIEW emp_view;"],
    ["ELSE", "Použití v podmínkách jako alternativa k IF.", "SELECT name, CASE WHEN age > 30 THEN 'Senior' ELSE 'Junior' END AS category FROM employees;"],
    ["FROM", "Určuje tabulku nebo pohled, ze kterého se vybírají data.", "SELECT * FROM employees;"],
    ["GROUP BY", "Seskupuje řádky se stejnými hodnotami ve specifikovaných sloupcích.", "SELECT department, COUNT(*) FROM employees GROUP BY department;"],
    ["GROUP_CONCAT()", "Spojuje hodnoty z více řádků do jednoho řetězce.", "SELECT GROUP_CONCAT(name) FROM employees;"],
    ["HAVING", "Podmínky na skupiny po použití GROUP BY.", "SELECT department, COUNT(*) FROM employees GROUP BY department HAVING COUNT(*) > 5;"],
    ["IN", "Kontrola, zda hodnota spadá do specifikované množiny hodnot.", "SELECT * FROM employees WHERE department IN ('HR', 'IT');"],
    ["LIMIT", "Omezuje počet výsledných řádků.", "SELECT * FROM employees LIMIT 10;"],
    ["ORDER BY", "Řadí výsledky podle jednoho nebo více sloupců.", "SELECT * FROM employees ORDER BY age DESC;"],
    ["REPLACE", "Nahrazuje text ve sloupci.", "SELECT REPLACE(name, 'a', 'o') FROM employees;"],
    ["SELECT (vnořený)", "Použití vnořeného výběru jako poddotazu.", "SELECT name FROM employees WHERE department_id IN (SELECT id FROM departments WHERE location = 'NY');"],
    ["SELECT", "Základní příkaz pro výběr dat z tabulky.", "SELECT name, age FROM employees;"],
    ["UPDATE", "Aktualizuje existující data v tabulce.", "UPDATE employees SET salary = salary * 1.1 WHERE department = 'IT';"],
    ["VIEWS", "Pohledy (views) jako uložené dotazy v databázi.", "CREATE VIEW high_salary AS SELECT * FROM employees WHERE salary > 50000;"],
    ["WHEN", "Použití s CASE pro specifikaci podmínek.", "SELECT name, CASE WHEN age > 30 THEN 'Senior' WHEN age > 20 THEN 'Mid' ELSE 'Junior' END AS category FROM employees;"],
    ["WHERE", "Podmínky pro filtrování řádků při výběru dat.", "SELECT * FROM employees WHERE age > 25;"],
    ["hodnoty", "Specifikace hodnot ve výběrech nebo podmínkách.", "SELECT * FROM employees WHERE salary = 50000;"],
    ["hvězdička (*)", "Výběr všech sloupců z tabulky.", "SELECT * FROM employees;"],
    ["logické operátory", "Operátory jako AND, OR, NOT pro spojování podmínek.", "SELECT * FROM employees WHERE age > 25 AND department = 'IT';"],
    ["podminka1", "Příklad použití základní podmínky v SQL dotazu.", "SELECT * FROM employees WHERE age > 30;"],
    ["podmínky", "Použití podmínek pro filtrování dat (WHERE, HAVING).", "SELECT * FROM employees WHERE department = 'HR';"],
    ["porovnávací operátory", "Operátory jako =, !=, >, <, >=, <=.", "SELECT * FROM employees WHERE salary > 40000;"],
    ["příkazy DBeaver", "Přehled základních příkazů podporovaných v DBeaver.", "SELECT * FROM employees;"],
    ["vnořený SELECT (poddotaz)", "Použití poddotazů (subquery) v SQL dotazu.", "SELECT name FROM employees WHERE department_id = (SELECT id FROM departments WHERE name = 'IT');"],
    ["základní příkaz", "Popis základních SQL příkazů.", "SELECT * FROM employees;"]
]

# Převod dat na Paragraph objekty pro automatické zalamování
processed_data = []
for row_idx, row in enumerate(data):
    processed_row = []
    for col_idx, cell in enumerate(row):
        if row_idx == 0:
            # Pro hlavičku použijeme odlišný styl
            processed_row.append(Paragraph(cell, styleH))
        else:
            processed_row.append(Paragraph(cell, styleN))
    processed_data.append(processed_row)

# Cesta k výstupnímu PDF souboru
pdf_output_path = "dbeaver_prikazy_prehled_vylepseny.pdf"

# Vytvoření dokumentu
doc = SimpleDocTemplate(
    pdf_output_path,
    pagesize=landscape(letter),
    rightMargin=30, leftMargin=30,
    topMargin=30, bottomMargin=18
)
elements = []

# Definice šířky sloupců (zvětšená šířka prvního sloupce)
col_widths = [200, 250, 400]  # Upravené šířky sloupců

# Vytvoření tabulky
table = Table(processed_data, colWidths=col_widths, repeatRows=1)

# Stylování tabulky
table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.grey),  # Hlavička
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),  # Barva textu hlavičky
    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),  # Zarovnání textu
    ('FONTNAME', (0, 0), (-1, 0), 'DejaVu'),  # Font hlavičky
    ('FONTSIZE', (0, 0), (-1, -1), 9),  # Velikost písma
    ('BOTTOMPADDING', (0, 0), (-1, 0), 6),  # Padding dolů pro hlavičku
    ('BACKGROUND', (0, 1), (-1, -1), colors.beige),  # Barva pozadí pro ostatní řádky
    ('GRID', (0, 0), (-1, -1), 0.5, colors.black),  # Okraje tabulky
    ('VALIGN', (0, 0), (-1, -1), 'TOP'),  # Vertikální zarovnání
]))

# Přidání tabulky do elementů
elements.append(table)

# Generování PDF
doc.build(elements)

print(f"PDF byl úspěšně vytvořen: {pdf_output_path}")

