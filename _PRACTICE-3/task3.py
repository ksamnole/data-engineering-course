import json
import xml.etree.ElementTree as ET

def getInfo(fileName):
  with open(fileName, "rb") as f:
        contents = f.read()
  root = ET.fromstring(contents)
  return {
      "name": root.find("name").text.strip(),
      "constellation": root.find("constellation").text.strip(),
      "spectral_class": root.find("spectral-class").text.strip(),
      "radius": int(root.find("radius").text),
      "rotation": root.find("rotation").text.strip(),
      "age": root.find("age").text.strip(),
      "distance": float(root.find("distance").text.split()[0]),
      "absolute_magnitude": float(root.find("absolute-magnitude").text.split()[0])
  }

result = []
for i in range(1, 500):
    result.append(getInfo(f"3/data/{i}.xml"))

copyResult = result

# Сортировка по радиусу
result = sorted(result, key=lambda x: int(x["radius"]), reverse=True)

# Фильтр только Возраст
result = list(filter(lambda x: float(x["age"].split()[0]) > 3, result))

# Статистика по Дистанции
distances = [int(item["distance"]) for item in copyResult]
_max = max(distances)
_min = min(distances)
avg = int(sum(distances) / len(distances))

print(f"Статистика по дистанции:")
print(f"Максимум: {_max}")
print(f"Минимум: {_min}")
print(f"В среднем: {avg}")
print("-------------------------")

# Частота знаков
constellations = [item.get("constellation", "NoNe") for item in copyResult]
freqRes = {}
for res in constellations:
    freqRes[res] = freqRes.get(res, 0) + 1
for res, freq in freqRes.items():
    print(f"{res}: {freq}")
print("-------------------------")

print(f"Всего записей получилось: {len(result)}")

with open('results/result_3.json', 'w', encoding='utf-8') as json_file:
    json.dump(result, json_file, ensure_ascii=False, indent=4)