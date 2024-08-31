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

def extrahuj_odkazy_obcí(soup):
    odkazy = []
    for řádek in soup.find_all('tr'):
        buňky = řádek.find_all('td')
        if len(buňky) >= 3:
            odkaz = buňky[0].find('a')
            if odkaz and 'href' in odkaz.attrs:
                href = odkaz['href']
                if 'ps311' in href or 'ps33' in href:
                    plná_url = f"https://volby.cz/pls/ps2017nss/{href}"
                    odkazy.append(plná_url)
    return odkazy

def scrapuj_data_obce(url):
    print(f"Zpracovávám URL: {url}")
    soup = získej_soup(url)
    if not soup:
        print(f"Nepodařilo se získat obsah stránky: {url}")
        return None

    try:
        # Získání kódu obce
        kód_element = soup.find('td', class_='cislo', headers='t1sa1 t1sb1')
        if kód_element and kód_element.a:
            kód = kód_element.a.text.strip()
        else:
            print("Nepodařilo se najít kód obce.")
            return None

        # Získání názvu obce
        h3_elementy = soup.find_all('h3')
        název_obce = None
        for h3 in h3_elementy:
            if "Obec:" in h3.text:
                název_obce = h3.text.split(":")[-1].strip()
                break
        if not název_obce:
            print("Nepodařilo se najít název obce.")
            return None

        # Získání voličů, vydaných obálek a platných hlasů
        tabulka = soup.find('table', {'id': 'ps311_t1'})
        if not tabulka:
            print("Nepodařilo se najít hlavní tabulku.")
            return None

        řádky = tabulka.find_all('tr')
        voliči = řádky[2].find_all('td')[3].text.strip().replace('\xa0', '')
        obálky = řádky[2].find_all('td')[4].text.strip().replace('\xa0', '')
        platné_hlasy = řádky[2].find_all('td')[7].text.strip().replace('\xa0', '')

        # Získání hlasů pro jednotlivé strany
        hlasy_stran = []
        tabulky_stran = soup.find_all('table', {'class': 'table'})
        for tabulka in tabulky_stran[1:]:  # Přeskočíme první tabulku, která obsahuje souhrnné informace
            řádky = tabulka.find_all('tr')[2:]  # Přeskočíme záhlaví tabulky
            for řádek in řádky:
                buňky = řádek.find_all('td')
                if len(buňky) >= 3:
                    hlasy = buňky[2].text.strip().replace('\xa0', '')
                    hlasy_stran.append(hlasy)

        return [kód, název_obce, voliči, obálky, platné_hlasy] + hlasy_stran

    except Exception as e:
        print(f"Chyba při zpracování {url}: {e}")
        return None
      
def ulož_výsledky_do_csv(data, výstupní_soubor):
    if not data:
        print("Žádná platná data k uložení.")
        return

    try:
        with open(výstupní_soubor, 'w', newline='', encoding='utf-8-sig') as soubor:
            writer = csv.writer(soubor)
            hlavičky = ["kód", "obec", "voliči", "vydané_obálky", "platné_hlasy"] + [f"strana_{i+1}" for i in range(len(data[0]) - 5)]
            writer.writerow(hlavičky)
            for řádek in data:
                writer.writerow(řádek)
        print(f"Data úspěšně uložena do {výstupní_soubor}")
        print(f"Počet uložených řádků: {len(data)}")
    except Exception as e:
        print(f"Chyba při ukládání dat do CSV: {e}")
        print(f"Pokus o uložení do: {výstupní_soubor}")

def main():
    parser = argparse.ArgumentParser(description="Scrapování volebních výsledků z roku 2017 pro vybranou správní jednotku.")
    parser.add_argument('url', type=str, help="URL správní jednotky ke scrapování.")
    parser.add_argument('výstupní_soubor', type=str, help="Název výstupního CSV souboru.")

    args = parser.parse_args()

    if not ověř_url(args.url):
        sys.exit(1)

    soup = získej_soup(args.url)
    if not soup:
        print("Nepodařilo se načíst vstupní stránku.")
        sys.exit(1)

    odkazy_obcí = extrahuj_odkazy_obcí(soup)
    
    if not odkazy_obcí:
        print("Nenalezeny žádné platné odkazy na obce.")
        sys.exit(1)

    všechna_data = []
    for odkaz in odkazy_obcí:
        print(f"Scrapuji data z {odkaz}...")
        data_obce = scrapuj_data_obce(odkaz)
        if data_obce:
            všechna_data.append(data_obce)
            print(f"Úspěšně získána data pro {data_obce[1]}")  # Vypíše název obce
        else:
            print(f"Nepodařilo se získat data pro {odkaz}")

    if not všechna_data:
        print("Nepodařilo se získat žádná platná data.")
        sys.exit(1)

    print(f"Celkem zpracováno obcí: {len(odkazy_obcí)}")
    print(f"Úspěšně získána data pro {len(všechna_data)} obcí")
    ulož_výsledky_do_csv(všechna_data, args.výstupní_soubor)

if __name__ == "__main__":
    main()