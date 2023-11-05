import json
import msgpack

dictionary = {}

with open('products_25.json') as f:
    products = json.load(f)

for product in products:
  name = product['name']
  price = float(product['price'])
  
  if name not in dictionary:
    dictionary[name] = {
      'avr': price,
      'min': price,
      'max': price,
      'count': 1
    }
  else:
    dictionary[name]['avr'] = (dictionary[name]['avr'] * dictionary[name]['count'] + price) / (dictionary[name]['count'] + 1)
    dictionary[name]['count'] += 1
    if price < dictionary[name]['min']:
      dictionary[name]['min'] = price
    if price > dictionary[name]['max']:
      dictionary[name]['max'] = price

with open(f"result3.json", "w") as file_stream:
    json.dump(dictionary, file_stream)
    file_stream.write('\n')

with open("result3.msgpack", "wb") as file_stream:
    packed = msgpack.packb(dictionary)
    file_stream.write(packed)