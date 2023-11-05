import csv
from bs4 import BeautifulSoup

rows = []

with open("text_5_var_25") as file: 
  soup = BeautifulSoup(file, "html.parser")
  elements = soup.find_all('tr')
  for element in elements:
    row = list(filter(lambda x: x != "", element.text.split('\n')))
    rows.append(row)

with open('result', 'w') as file:
  csv_writer = csv.writer(file)
  csv_writer.writerows(rows)
