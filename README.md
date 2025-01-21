Engeto-pa-3-projekt

Třetí projekt na Python Akademii od Engeta.

Tento skript slouží ke scrapování volebních výsledků z roku 2017 pro vybranou správní jednotku.
Autor

Jméno: Miroslav Coufalik
Email: mira.coufa@gmail.com
Discord: 88barcode88#1001

Popis projektu
Tento program stahuje volební data z webu volby.cz pro zadanou územní jednotku a ukládá je do CSV souboru. Scrapuje informace jako kód obce, název obce, počet voličů, vydané obálky, platné hlasy a hlasy pro jednotlivé kandidující strany.
Instalace

Naklonujte tento repozitář:
git clone https://github.com/88barcode88/Engeto-Projekty-Python-MC.git
cd Engeto-Projekty-Python-MC

Vytvořte virtuální prostředí:
python -m venv venv

Aktivujte virtuální prostředí:
..\venv\Scripts\activate

Windows: venv\Scripts\activate
macOS/Linux: source venv/bin/activate

Po aktivaci byste měli vidět (venv) na začátku příkazového řádku, což indikuje, že virtuální prostředí je aktivní.

Nainstalujte potřebné knihovny:
pip install -r requirements.txt

Použití
Program se spouští z příkazové řádky a vyžaduje dva argumenty:

URL adresu územního celku ke scrapování
Název výstupního CSV souboru

Příklad použití:
python projekt_3.py  <odkaz-uzemniho-celku> <vysledny-soubor.csv>
U mého přiloženého souboru to je:
python projekt_3.py "https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=12&xnumnuts=7103" "vysledky_prostejov.csv"

Průběh stahování:
Zpracovávám URL: https://volby.cz/pls/ps2017nss/ps311?xjazyk=CZ&xkraj=12&xobec=590240&xvyber=7103
Úspěšně načtena stránka: https://volby.cz/pls/ps2017nss/ps311?xjazyk=CZ&xkraj=12&xobec=590240&xvyber=7103
Úspěšně získána data pro Želeč
Data úspěšně uložena do vysledky_prostejov.csv

částečný výstup:
Po úspěšném spuštění program vytvoří CSV soubor s následující strukturou:
kód obce,název obce,voliči v seznamu,vydané obálky,platné hlasy,Občanská demokratická strana,Řád národa - Vlastenecká unie,...
506761,Alojzov,205,145,144,29,0,...
589268,Bedihošť,834,527,524,51,0,...
...

Po kontrole nezapomeňte ukončit virtualní prostředí. Pro deaktivaci virtuálního prostředí použijte:
deactivate
