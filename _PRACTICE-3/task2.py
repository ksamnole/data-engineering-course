import json
from operations import sorting
from bs4 import BeautifulSoup

def getCharacteristics(info, item):
    props = item.ul.find_all("li")
    for prop in props:
        info[prop["type"]] = prop.get_text().strip()

def getProductsInfo(fileName):

    with open(fileName, "rb") as f:
        contents = f.read()
        soup = BeautifulSoup(contents, 'html.parser')

    all_product_info = []
    product_items = soup.find_all('div', {'class': 'product-item'})
    for item in product_items:
        product_info = {}
        product_info['id'] = item.find('a', {'class': 'add-to-favorite'}).get('data-id')
        product_info['title'] = item.find('span').text.strip()
        product_info['price'] = item.find('price').text.strip()
        product_info['bonus'] = item.find('strong').text.split(' ')[2].strip()

        getCharacteristics(product_info, item)

        all_product_info.append(product_info)
    
    return all_product_info

result = []
for i in range(1, 45):
    result.extend(getProductsInfo(f"2/data/{i}.html"))

copyResult = result

# Сортировка по цене
result = sorted(result, key=lambda x: float("".join(x["price"][:-2].split(" "))), reverse=True)

# Фильтр только AMOLED
result = list(filter(lambda x: x.get("matrix", None) == "AMOLED", result))

# Статистика по RAM
ram = []
for item in copyResult:
    if ("ram" in item.keys()):
        ram.append(int(item["ram"][:-3]))
maxRam = max(ram)
minRam = min(ram)
avgRam = int(sum(ram) / len(ram))

print(f"Статистика по просмотрам:")
print(f"Максимум: {maxRam}")
print(f"Минимум: {minRam}")
print(f"В среднем: {avgRam}")
print("-------------------------")

# Частота разрешений
resolutions = [item.get("resolution", "NoNe") for item in copyResult]
freqRes = {}
for res in resolutions:
    freqRes[res] = freqRes.get(res, 0) + 1
for res, freq in freqRes.items():
    print(f"{res}: {freq}")
print("-------------------------")

print(f"Всего записей получилось: {len(result)}")

# Вывод данных в JSON
with open('results/result_2.json', 'w', encoding='utf-8') as json_file:
    json.dump(result, json_file, ensure_ascii=False, indent=4)