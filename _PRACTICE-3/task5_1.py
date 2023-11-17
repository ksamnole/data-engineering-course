import requests
import json
from bs4 import BeautifulSoup

fish_links = ["https://rf4.info/_/ide/", 
              "https://rf4.info/_/brown_trout/",
              "https://rf4.info/_/sterlet/",
              "https://rf4.info/_/pontic_shad/",
              "https://rf4.info/_/siberian_sculpin/",
              "https://rf4.info/_/opah/",
              "https://rf4.info/_/siberian_lamprey/",
              "https://rf4.info/_/baikal_omul/",
              "https://rf4.info/_/nelma/",
              "https://rf4.info/_/whiting/",
              "https://rf4.info/_/edible_crab/"
              ]
result = []

def getCharacteristics(info, item):
  props = item.find_all('div')
  for prop in props:
    info[prop["id"]] = prop.get_text().strip()

def addHabitat(info, places):
  info["habitat"] = []
  for place in places:
    plc = place.a.text
    if plc not in info["habitat"]:
      info["habitat"].append(plc)

for url in fish_links:
  response = requests.get(url)

  if response.status_code == 200:
    soup = BeautifulSoup(response.text, "html.parser")
  
  fish_info = {}

  desc = soup.find('details', {'class': 'fish_info_desc'})
  if desc is not None:
    fish_info["name"] = desc.find('summary').h2.text.split()[1]
    fish_info["desctription"] = "\n".join([x.get_text() for x in  desc.find('div').find_all('p')])

  fish_info_data = soup.find('div', {'class': 'fish_info_data'})
  getCharacteristics(fish_info, fish_info_data)

  places = soup.find_all('td', {'class': 'tbl-loc'})
  addHabitat(fish_info, places)

  result.append(fish_info)

copyResult = result

# Сортировка по количеству мест обитания
result = sorted(result, key=lambda x: len(x["habitat"]), reverse=True)

# Фильтр рыбы которые есть в р.Белая
result = list(filter(lambda x: "р.Белая" in x["habitat"], result))

# Статистика по f_min
f_mins = []
for item in result:
  if "f_min" in item.keys():
    f_mins.append(int(item["f_min"].replace(",", "")))
_max = max(f_mins)
_min = min(f_mins)
avg = int(sum(f_mins) / len(f_mins))

print(f"Статистика по f_mins:")
print(f"Максимум: {_max}")
print(f"Минимум: {_min}")
print(f"В среднем: {avg}")
print("-------------------------")

# Частота знаков
habitats = []
for item in copyResult:
  for habitat in item["habitat"]:
    habitats.append(habitat)
freqRes = {}
for res in habitats:
    freqRes[res] = freqRes.get(res, 0) + 1
for res, freq in freqRes.items():
    print(f"{res}: {freq}")
print("-------------------------")

print(f"Всего записей получилось: {len(result)}")

with open('results/result_5_1.json', 'w', encoding='utf-8') as json_file:
  json.dump(result, json_file, ensure_ascii=False, indent=4)