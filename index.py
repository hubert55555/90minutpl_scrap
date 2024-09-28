from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import csv
import os

wyborStrony = ['http://www.90minut.pl/liga/1/liga13482.html', 'http://www.90minut.pl/liga/1/liga13483.html', 'http://www.90minut.pl/liga/1/liga13484.html']

### USTAW ZMIENNE ###
# Ekstraklasa = 0       I liga = 1          II liga = 2
strona = 0


driver_path = "msedgedriver.exe" #Microsoft Edge
service = Service(driver_path)
driver = webdriver.Edge(service=service)
nazwaPliku = 'dane.csv'

driver.get(wyborStrony[strona])

dane = []
table = driver.find_element(By.XPATH, '/html/body/table[2]/tbody/tr[1]/td[3]/p[4]/table')
rows = table.find_elements(By.TAG_NAME, 'tr')

for row in rows:
    cells = row.find_elements(By.TAG_NAME, 'td') or row.find_elements(By.TAG_NAME, 'th')
    cell_data = [cell.text.replace(" ", "") for cell in cells]
    dane.append(cell_data)

with open(nazwaPliku, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file, delimiter=';')  # Use ';' as delimiter for columns
    writer.writerows(dane)

tabela = []

with open(nazwaPliku, newline='', encoding='utf-8') as plik_csv:
    czytnik_csv = csv.reader(plik_csv, delimiter=';')
    for wiersz in czytnik_csv:
        wiersz_bez_drugiej_kolumny = wiersz[:1] + wiersz[2:]
        tabela.append(wiersz_bez_drugiej_kolumny)

driver.quit()

# Słownik przechowujący dane o klubach
kluby_statystyki = {}

# Inicjalizowanie danych dla każdego klubu
for i in range(1, 19):
    kluby_statystyki[i] = {
        'strzelone_gospodarz': [],
        'stracone_gospodarz': [],
        'strzelone_wyjazd': [],
        'stracone_wyjazd': []
    }

# Przetwarzanie danych
for row_idx in range(1, len(tabela)):
    for col_idx in range(1, len(tabela[row_idx])):
        wynik = tabela[row_idx][col_idx]
        if wynik:  # Jeżeli komórka nie jest pusta
            # Podziel wynik na bramki gospodarza i gościa
            bramki_gospodarza, bramki_goscia = map(int, wynik.split('-'))

            # Numery klubów
            klub_gospodarz = int(tabela[row_idx][0])
            klub_gosc = int(tabela[0][col_idx])

            # Aktualizuj statystyki dla gospodarza
            kluby_statystyki[klub_gospodarz]['strzelone_gospodarz'].append(bramki_gospodarza)
            kluby_statystyki[klub_gospodarz]['stracone_gospodarz'].append(bramki_goscia)

            # Aktualizuj statystyki dla gościa
            kluby_statystyki[klub_gosc]['strzelone_wyjazd'].append(bramki_goscia)
            kluby_statystyki[klub_gosc]['stracone_wyjazd'].append(bramki_gospodarza)

os.remove("statystyki_klubow.txt")

# Zapisywanie wyników do pliku
with open('statystyki_klubow.txt', 'w') as f:
    for klub, stats in kluby_statystyki.items():
        # Zapis strzelonych bramek jako gospodarza
        f.write(f"{klub}, " + ", ".join(map(str, stats['strzelone_gospodarz'])) + "\n")
        # Zapis straconych bramek jako gospodarza
        f.write(f"{klub}, " + ", ".join(map(str, stats['stracone_gospodarz'])) + "\n")
        # Zapis strzelonych bramek na wyjeździe
        f.write(f"{klub}, " + ", ".join(map(str, stats['strzelone_wyjazd'])) + "\n")
        # Zapis straconych bramek na wyjeździe
        f.write(f"{klub}, " + ", ".join(map(str, stats['stracone_wyjazd'])) + "\n")

os.remove("dane.csv")
print("Statystyki klubów zostały zapisane do pliku 'statystyki_klubow.txt'.")