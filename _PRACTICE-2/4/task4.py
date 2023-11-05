import json
import pickle

with open('products_25.pkl', 'rb') as pkl_file:
	products = dict(map(lambda x: (x["name"], x["price"]), pickle.load(pkl_file)))

with open('price_info_25.json') as json_file:
    price_info = json.load(json_file)

for info in price_info:
	method = info['method']
	if method == 'add':
		products[info['name']] += info['param']
	elif method == 'sub':
		products[info['name']] -= info['param']
	elif method == 'percent+':
		products[info['name']] = products[info['name']] * (1 + info['param'])
	elif method == 'percent-':
		products[info['name']] = products[info['name']] * (1 - info['param'])

output = [{'name': k, 'price': v} for k,v in products.items()]

with open("result.pkl", "wb") as file:
    file.write(pickle.dumps(output))