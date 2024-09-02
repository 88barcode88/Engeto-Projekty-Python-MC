"""
projekt_3.py: druhý projekt do Engeto Online Python Akademie

author: Miroslav Coufalik
email: mira.coufa@gmail.com
discord: 88barcode88#1001
"""


import requests
from bs4 import BeautifulSoup
import csv
import sys
import argparse


def ověř_url(url):
    try:
        odpověď = requests.get(url)
        if odpověď.status_code == 200:
            return True
        else:
            print(f"Chyba: URL není dostupná. Stavový kód: {odpověď.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"Chyba: Neplatná URL nebo problém se sítí. Detaily: {e}")
        return False

def získej_soup(url):
    try:
        odpověď = requests.get(url)
        odpověď.raise_for_status()
        print(f"Úspěšně načtena stránka: {url}")
        return BeautifulSoup(odpověď.text, 'html.parser')
    except requests.RequestException as e:
        print(f"Chyba při načítání stránky {url}: {e}")
        return None

def extrahuj_kódy_a_názvy_obcí(url):
    soup = získej_soup(url)
    if not soup:
        return None, None

    odkazy_obcí = []
    kódy_a_názvy = {}
    
    for řádek in soup.find_all('tr'):
        buňky = řádek.find_all('td')
        if len(buňky) >= 3:
            odkaz = buňky[0].find('a')
            if odkaz and 'href' in odkaz.attrs:
                href = odkaz['href']
                kód_obce = odkaz.text.strip()
                název_obce = buňky[1].text.strip()
                plná_url = f"https://volby.cz/pls/ps2017nss/{href}"
                
                odkazy_obcí.append(plná_url)
                kódy_a_názvy[kód_obce] = název_obce
    
    return odkazy_obcí, kódy_a_názvy

def scrapuj_data_obce(url, kód_obce, kódy_a_názvy):
    print(f"Zpracovávám URL: {url}")
    soup = získej_soup(url)
    if not soup:
        print(f"Nepodařilo se získat obsah stránky: {url}")
        return None

    try:
        # Získání volebních údajů pro obec
        voliči_element = soup.find('td', class_='cislo', headers='sa2')
        voliči = voliči_element.text.strip().replace('\xa0', '') if voliči_element else '0'

        obálky_element = soup.find('td', class_='cislo', headers='sa5')
        obálky = obálky_element.text.strip().replace('\xa0', '') if obálky_element else '0'

        platné_hlasy_element = soup.find('td', class_='cislo', headers='sa6')
        platné_hlasy = platné_hlasy_element.text.strip().replace('\xa0', '') if platné_hlasy_element else '0'

        # Získání hlasů a čísel pro jednotlivé strany
        hlasy_stran = []
        for tabulka in soup.find_all('div', class_='t2_470'):
            řádky = tabulka.find_all('tr')
            for řádek in řádky[1:]:  # Přeskočíme záhlaví tabulky
                buňky = řádek.find_all('td')
                if len(buňky) >= 3:
                    číslo_strany_element = buňky[0]
                    název_strany_element = buňky[1]
                    hlasy_element = buňky[2]

                    číslo_strany = int(číslo_strany_element.text.strip()) if číslo_strany_element.text.strip().isdigit() else 0
                    název_strany = název_strany_element.text.strip() if název_strany_element else '0'
                    hlasy = hlasy_element.text.strip().replace('\xa0', '') if hlasy_element else '0'

                    if číslo_strany != 0:
                        hlasy_stran.append((číslo_strany, název_strany, hlasy))

        # Seřazení stran podle jejich čísla
        hlasy_stran.sort(key=lambda x: x[0])

        název_obce = kódy_a_názvy.get(kód_obce, 'Neznámá obec')
        return [kód_obce, název_obce, voliči, obálky, platné_hlasy, hlasy_stran]

    except Exception as e:
        print(f"Chyba při zpracování {url}: {e}")
        return None

def ulož_výsledky_do_csv(data, výstupní_soubor):
    if not data:
        print("Žádná platná data k uložení.")
        return

    try:
        # Získání všech stran a jejich čísel
        všechny_strany = {}
        for obec_data in data:
            for číslo, název, _ in obec_data[5]:
                všechny_strany[číslo] = název

        # Seřazení stran podle jejich čísla
        seřazené_strany = sorted(všechny_strany.items())

        hlavičky = ["kód obce", "název obce", "voliči v seznamu", "vydané obálky", "platné hlasy"] + [název for _, název in seřazené_strany]

        with open(výstupní_soubor, 'w', newline='', encoding='utf-8-sig') as soubor:
            writer = csv.writer(soubor)
            writer.writerow(hlavičky)

            for obec_data in data:
                řádek = obec_data[:5]
                strany_hlasy = {číslo: '0' for číslo, _ in seřazené_strany}
                for číslo, _, hlasy in obec_data[5]:
                    strany_hlasy[číslo] = hlasy
                řádek += [strany_hlasy[číslo] for číslo, _ in seřazené_strany]
                writer.writerow(řádek)

        print(f"Data úspěšně uložena do {výstupní_soubor}")

    except Exception as e:
        print(f"Chyba při ukládání dat do CSV: {e}")

def main():
    parser = argparse.ArgumentParser(description="Scrapování volebních výsledků z roku 2017 pro vybranou správní jednotku.")
    parser.add_argument('url', type=str, help="URL správní jednotky ke scrapování.")
    parser.add_argument('výstupní_soubor', type=str, help="Název výstupního CSV souboru.")

    args = parser.parse_args()

    if not ověř_url(args.url):
        sys.exit(1)

    odkazy_obcí, kódy_a_názvy = extrahuj_kódy_a_názvy_obcí(args.url)
    
    if not odkazy_obcí:
        print("Nenalezeny žádné platné odkazy na obce.")
        sys.exit(1)

    všechna_data = []
    for odkaz in odkazy_obcí:
        kód_obce = odkaz.split("xobec=")[1].split("&")[0]  # Extract the code from the URL
        data_obce = scrapuj_data_obce(odkaz, kód_obce, kódy_a_názvy)
        if data_obce:
            všechna_data.append(data_obce)
            print(f"Úspěšně získána data pro {data_obce[1]}")  # Vypíše název obce
        else:
            print(f"Nepodařilo se získat data pro {odkaz}")

    if not všechna_data:
        print("Nepodařilo se získat žádná platná data.")
        sys.exit(1)

    ulož_výsledky_do_csv(všechna_data, args.výstupní_soubor)

if __name__ == "__main__":
    main()