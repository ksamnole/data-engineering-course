import json
from bs4 import BeautifulSoup

def getBuildingInfo(fileName):
    with open(fileName, "rb") as f:
        contents = f.read()
        soup = BeautifulSoup(contents, 'html.parser')

    building_info = {}
    building_info['город'] = soup.find('div', {'class': 'build-wrapper'}).find('div').span.text.split(":")[1].strip()
    building_info['название'] = soup.find('h1', {'class': 'title'}).text.strip()

    address_data = soup.find('p', {'class': 'address-p'}).text.split('Индекс:')
    building_info['улица'] = address_data[0].replace('Улица: ', '').strip()
    building_info['индекс'] = address_data[1].strip()

    spans = [x.get_text() for x in soup.find_all('span')]
    building_info['этажи'] = soup.find('span', {'class': 'floors'}).text.split(': ')[1].strip()
    building_info['год_постройки'] = soup.find('span', {'class': 'year'}).text.split(' ')[-1].strip()
    building_info['парковка'] = 'есть' if 'Парковка:есть' in spans else 'нет'
    building_info['рейтинг'] = soup.find('div', {'class': 'build-wrapper'}).find_all('span')[-2].text.split(': ')[1].strip()
    building_info['просмотры'] = soup.find('div', {'class': 'build-wrapper'}).find_all('span')[-1].text.split(': ')[1].strip()

    return building_info

result = []
for i in range(1, 999):
    result.append(getBuildingInfo(f"1/data/{i}.html"))

copyResult = result

# Сортировка по рейтингу
result = sorted(result, key=lambda x: float(x["рейтинг"]), reverse=True)

# Фильтр больше 5 этажей
result = list(filter(lambda x: int(x["этажи"]) > 5, result))

# Статистика по  просмотрам
views = [int(item["просмотры"]) for item in copyResult]
maxViews = max(views)
minViews = min(views)
avgViews = int(sum(views) / len(views))

print(f"Статистика по просмотрам:")
print(f"Максимум: {maxViews}")
print(f"Минимум: {minViews}")
print(f"В среднем: {avgViews}")
print("-------------------------")

# Частота городов
cities = [item["город"] for item in copyResult]
freqCities = {}
for city in cities:
    freqCities[city] = freqCities.get(city, 0) + 1
for city, freq in freqCities.items():
    print(f"{city}: {freq}")
print("-------------------------")

print(f"Всего записей получилось: {len(result)}")

with open('results/result_1.json', 'w', encoding='utf-8') as json_file:
    json.dump(result, json_file, ensure_ascii=False, indent=4)