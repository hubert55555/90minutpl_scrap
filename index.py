from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import csv

wyborStrony = ['http://www.90minut.pl/liga/1/liga13482.html', 'http://www.90minut.pl/liga/1/liga13483.html', 'http://www.90minut.pl/liga/1/liga13484.html']

### USTAW ZMIENNE ###
# Ekstraklasa = 0       I liga = 1          II liga = 2
strona = 0
nazwaPliku = 'dane.csv'

driver_path = "msedgedriver.exe" #Microsoft Edge
service = Service(driver_path)
driver = webdriver.Edge(service=service)

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

driver.quit()
