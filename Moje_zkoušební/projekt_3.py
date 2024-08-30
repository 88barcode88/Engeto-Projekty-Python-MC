"""
projekt_3.py: třetí projekt do Engeto Online Python Akademie

author: Miroslav Coufalik
email: mira.coufa@gmail.com
discord: 88barcode88#1001
"""

import sys
import requests
from bs4 import BeautifulSoup
import csv
import argparse

def validate_url(url):
    """Validuje, zda je URL správně formátovaná a dostupná."""
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return True
        else:
            print(f"Chyba: URL není dostupná. Status code: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"Chyba: Neplatná URL nebo problém se sítí. Detaily: {e}")
        return False

def get_soup(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for bad status codes
        print(f"Úspěšně načtena stránka: {url}")
        return BeautifulSoup(response.text, 'html.parser')
    except requests.RequestException as e:
        print(f"Chyba při načítání stránky {url}: {e}")
        return None

def extract_municipality_links(soup):
    """Extrahuje odkazy na všechny obce z dané stránky."""
    links = []
    tables = soup.find_all('table', {'class': 'table'})
    for table in tables:
        rows = table.find_all('tr')
        for row in rows[1:]:  # Přeskočíme hlavičku tabulky
            cells = row.find_all('td')
            if len(cells) >= 2:
                link = cells[0].find('a')
                if link:
                    href = link.get('href')
                    if href:
                        links.append(f"https://volby.cz/pls/ps2017nss/{href}")
    return links

def scrape_municipality_data(url):
    """Stáhne data z výsledků jedné obce."""
    print(f"Zpracovávám URL: {url}")
    soup = get_soup(url)
    if not soup:
        print(f"Nepodařilo se získat obsah stránky: {url}")
        return None

    try:
        # Hledáme kód obce a název obce
        code_element = soup.find('td', {'class': 'cislo'})
        if code_element:
            code = code_element.text.strip()
        else:
            print("Kód obce nebyl nalezen.")
            return None

        name_element = soup.find('h3')
        if name_element:
            name = name_element.text.strip().split(':')[-1].strip()
        else:
            print("Název obce nebyl nalezen.")
            return None

        print(f"Nalezeno: Kód obce: {code}, Název obce: {name}")

        voters = soup.select_one('td[headers="sa2"]')
        envelopes = soup.select_one('td[headers="sa3"]')
        valid_votes = soup.select_one('td[headers="sa6"]')
        
        voters = voters.text.replace('\xa0', '') if voters else '0'
        envelopes = envelopes.text.replace('\xa0', '') if envelopes else '0'
        valid_votes = valid_votes.text.replace('\xa0', '') if valid_votes else '0'
        
        print(f"Základní data: Voliči: {voters}, Obálky: {envelopes}, Platné hlasy: {valid_votes}")
        
        # Najdeme tabulku s výsledky stran
        results_table = soup.find('table', {'class': 'table'})
        if not results_table:
            print(f"Nenalezena tabulka s výsledky na URL: {url}")
            return None
        
        # Získáme počty hlasů (přeskakujeme názvy stran)
        votes = []
        vote_cells = results_table.select('td[headers="t1sa2 t1sb3"], td[headers="t2sa2 t2sb3"]')
        for cell in vote_cells:
            votes.append(cell.text.replace('\xa0', '').replace(',', '').strip())
        
        if not votes:
            print(f"Nenalezeny žádné hlasy na URL: {url}")
            return None

        print(f"Nalezeno {len(votes)} výsledků hlasování.")

        return [code, name, voters, envelopes, valid_votes] + votes

    except Exception as e:
        print(f"Chyba při zpracování {url}: {e}")
        return None
    
def save_results_to_csv(data, output_file):
    """Uloží data do CSV souboru."""
    valid_data = [row for row in data if row is not None]
    if not valid_data:
        print("Žádná platná data k uložení.")
        return

    try:
        # Získáme názvy stran z prvního záznamu, pokud existuje
        num_parties = len(valid_data[0]) - 5 if valid_data else 0
        headers = ["Kód obce", "Název obce", "Voliči v seznamu", "Vydané obálky", "Platné hlasy"] + [f"Strana {i+1}" for i in range(num_parties)]
        
        with open(output_file, 'w', newline='', encoding='utf-8-sig') as file:
            writer = csv.writer(file)
            writer.writerow(headers)
            for row in valid_data:
                writer.writerow(row)

        print(f"Data byla uložena do souboru {output_file}. Celkem uloženo {len(valid_data)} záznamů.")
    except Exception as e:
        print(f"Chyba při ukládání dat do souboru: {e}")

def main():
    parser = argparse.ArgumentParser(description="Scrape výsledků voleb z roku 2017 pro zvolený územní celek.")
    parser.add_argument('url', type=str, help="URL územního celku ke scrapování.")
    parser.add_argument('output_file', type=str, help="Název výstupního CSV souboru.")

    args = parser.parse_args()

    soup = get_soup(args.url)
    if not soup:
        print("Nepodařilo se načíst vstupní stránku.")
        sys.exit(1)

    municipality_links = extract_municipality_links(soup)
    
    if not municipality_links:
        print("Nenalezeny žádné platné odkazy na obce.")
        sys.exit(1)

    all_data = []
    for link in municipality_links:
        print(f"Scrapuji data z {link}...")
        municipality_data = scrape_municipality_data(link)
        if municipality_data:
            all_data.append(municipality_data)
        else:
            print(f"Nepodařilo se získat data pro {link}")

    if not all_data:
        print("Nepodařilo se získat žádná platná data.")
        sys.exit(1)

    save_results_to_csv(all_data, args.output_file)

if __name__ == "__main__":
    main()
