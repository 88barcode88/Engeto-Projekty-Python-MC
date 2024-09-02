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

def zkontroluj_dostupnost_url(url):
    """Zkontroluje, zda je zadaná URL adresa dostupná."""
    try:
        odpoved = requests.get(url)
        if odpoved.status_code == 200:
            return True
        else:
            print(f"Chyba: URL není dostupná. Stavový kód: {odpoved.status_code}")
            return False
    except requests.exceptions.RequestException as chyba:
        print(f"Chyba: Neplatná URL nebo problém se sítí. Detaily: {chyba}")
        return False

def nacti_html_stranku(url):
    """Načte HTML obsah stránky a vrátí ho jako BeautifulSoup objekt."""
    try:
        odpoved = requests.get(url)
        odpoved.raise_for_status()
        print(f"Úspěšně načtena stránka: {url}")
        return BeautifulSoup(odpoved.text, 'html.parser')
    except requests.RequestException as chyba:
        print(f"Chyba při načítání stránky {url}: {chyba}")
        return None

def ziskej_odkazy_a_nazvy_obci(url):
    """Získá odkazy na obce a jejich názvy z hlavní stránky."""
    soup = nacti_html_stranku(url)
    if not soup:
        return None, None

    odkazy_obci = []
    kody_a_nazvy = {}
    
    for radek in soup.find_all('tr'):
        bunky = radek.find_all('td')
        if len(bunky) >= 3:
            odkaz = bunky[0].find('a')
            if odkaz and 'href' in odkaz.attrs:
                href = odkaz['href']
                kod_obce = odkaz.text.strip()
                nazev_obce = bunky[1].text.strip()
                plna_url = f"https://volby.cz/pls/ps2017nss/{href}"
                
                odkazy_obci.append(plna_url)
                kody_a_nazvy[kod_obce] = nazev_obce
    
    return odkazy_obci, kody_a_nazvy

def ziskej_data_obce(url, kod_obce, kody_a_nazvy):
    """Získá volební data pro konkrétní obec."""
    print(f"Zpracovávám URL: {url}")
    soup = nacti_html_stranku(url)
    if not soup:
        print(f"Nepodařilo se získat obsah stránky: {url}")
        return None

    try:
        # Získání základních volebních údajů pro obec
        volici = soup.find('td', class_='cislo', headers='sa2').text.strip().replace('\xa0', '')
        obalky = soup.find('td', class_='cislo', headers='sa5').text.strip().replace('\xa0', '')
        platne_hlasy = soup.find('td', class_='cislo', headers='sa6').text.strip().replace('\xa0', '')

        # Získání hlasů pro jednotlivé strany
        hlasy_stran = []
        for tabulka in soup.find_all('div', class_='t2_470'):
            radky = tabulka.find_all('tr')
            for radek in radky[1:]:  # Přeskočíme záhlaví tabulky
                bunky = radek.find_all('td')
                if len(bunky) >= 3:
                    cislo_strany = int(bunky[0].text.strip())
                    nazev_strany = bunky[1].text.strip()
                    pocet_hlasu = bunky[2].text.strip().replace('\xa0', '')
                    hlasy_stran.append((cislo_strany, nazev_strany, pocet_hlasu))

        # Seřazení stran podle jejich čísla
        hlasy_stran.sort(key=lambda x: x[0])

        nazev_obce = kody_a_nazvy.get(kod_obce, 'Neznámá obec')
        return [kod_obce, nazev_obce, volici, obalky, platne_hlasy, hlasy_stran]

    except Exception as chyba:
        print(f"Chyba při zpracování {url}: {chyba}")
        return None

def uloz_vysledky_do_csv(data, vystupni_soubor):
    """Uloží získaná data do CSV souboru."""
    if not data:
        print("Žádná platná data k uložení.")
        return

    try:
        # Získání všech stran a jejich čísel
        vsechny_strany = {}
        for obec_data in data:
            for cislo, nazev, _ in obec_data[5]:
                vsechny_strany[cislo] = nazev

        # Seřazení stran podle jejich čísla
        serazene_strany = sorted(vsechny_strany.items())

        hlavicky = ["kód obce", "název obce", "voliči v seznamu", "vydané obálky", "platné hlasy"] + [nazev for _, nazev in serazene_strany]

        with open(vystupni_soubor, 'w', newline='', encoding='utf-8-sig') as soubor:
            writer = csv.writer(soubor)
            writer.writerow(hlavicky)

            for obec_data in data:
                radek = obec_data[:5]
                strany_hlasy = {cislo: '0' for cislo, _ in serazene_strany}
                for cislo, _, hlasy in obec_data[5]:
                    strany_hlasy[cislo] = hlasy
                radek += [strany_hlasy[cislo] for cislo, _ in serazene_strany]
                writer.writerow(radek)

        print(f"Data úspěšně uložena do {vystupni_soubor}")

    except Exception as chyba:
        print(f"Chyba při ukládání dat do CSV: {chyba}")

def main():
    parser = argparse.ArgumentParser(description="Scrapování volebních výsledků z roku 2017 pro vybranou správní jednotku.")
    parser.add_argument('url', type=str, help="URL správní jednotky ke scrapování.")
    parser.add_argument('vystupni_soubor', type=str, help="Název výstupního CSV souboru.")

    args = parser.parse_args()

    if not zkontroluj_dostupnost_url(args.url):
        sys.exit(1)

    odkazy_obci, kody_a_nazvy = ziskej_odkazy_a_nazvy_obci(args.url)
    
    if not odkazy_obci:
        print("Nenalezeny žádné platné odkazy na obce.")
        sys.exit(1)

    vsechna_data = []
    for odkaz in odkazy_obci:
        kod_obce = odkaz.split("xobec=")[1].split("&")[0]  # Extrahujeme kód obce z URL
        data_obce = ziskej_data_obce(odkaz, kod_obce, kody_a_nazvy)
        if data_obce:
            vsechna_data.append(data_obce)
            print(f"Úspěšně získána data pro {data_obce[1]}")  # Vypíše název obce
        else:
            print(f"Nepodařilo se získat data pro {odkaz}")

    if not vsechna_data:
        print("Nepodařilo se získat žádná platná data.")
        sys.exit(1)

    uloz_vysledky_do_csv(vsechna_data, args.vystupni_soubor)

if __name__ == "__main__":
    main()