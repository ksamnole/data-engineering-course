import requests
import json
from bs4 import BeautifulSoup

fish_links = ["https://rf4.info/mosquito_lake/", 
              "https://rf4.info/winding_rivulet/",
              "https://rf4.info/old_burg_lake/",
              "https://rf4.info/belaya_river/",
              "https://rf4.info/bear_lake/",
              "https://rf4.info/ladoga_lake/",
              "https://rf4.info/the_amber_lake/",
              "https://rf4.info/ladoga_archipelago/",
              "https://rf4.info/akhtuba_river/",
              "https://rf4.info/yama_river/",
              ]
result = []

def getFishes(lake_info, trs):
  lake_info['fishes'] = []
  for tr in trs:
    if tr.find('th') is not None:
      continue
    fish = {}
    fish['fish-name'] = tr.find('td', {'class': 'tbl-fish'}).a.text
    fish['massa'] = tr.find('td', {'class': 'tbl-weight'}).text
    fish['count'] = tr.find('td', {'class': 'tbl-count'}).text
    fish['price'] = tr.find('td', {'class': 'tbl-price'}).text
    lake_info['fishes'].append(fish)

for url in fish_links:
  response = requests.get(url)

  if response.status_code == 200:
    soup = BeautifulSoup(response.text, "html.parser")
  
  lake_info = {}
  lake_info["name"] = soup.find('select').find('option', selected=True).text

  trs = soup.find('table', {'id': 'tbl'}).find_all('tr')
  
  getFishes(lake_info, trs)

  result.append(lake_info)

copyResult = result

# Сортировка по сумме масс рыбы, которая водится в озере
result = sorted(result, key=lambda x: sum([int(y['massa'].replace(',', '')) for y in x['fishes']]), reverse=True)

# Фильтр у которых больше 15 рыб
result = list(filter(lambda x: len(x['fishes']) > 15, result))

# Статистика по massa
f_mins = []
for item in result:
    f_mins.extend([int(y['massa'].replace(',', '')) for y in item['fishes']])
_max = max(f_mins)
_min = min(f_mins)
avg = int(sum(f_mins) / len(f_mins))

print(f"Статистика по массам рыб:")
print(f"Максимум: {_max}")
print(f"Минимум: {_min}")
print(f"В среднем: {avg}")
print("-------------------------")

# Частота знаков: по рыбам
fishes = []
for item in copyResult:
  for fish in item["fishes"]:
    fishes.append(fish['fish-name'])
freqRes = {}
for res in fishes:
    freqRes[res] = freqRes.get(res, 0) + 1
for res, freq in freqRes.items():
    print(f"{res}: {freq}")
print("-------------------------")

print(f"Всего записей получилось: {len(result)}")

with open('results/result_5_2.json', 'w', encoding='utf-8') as json_file:
  json.dump(result, json_file, ensure_ascii=False, indent=4)