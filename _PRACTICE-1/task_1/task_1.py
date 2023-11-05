frequency = dict()

with open("text_1_var_25") as file:
    lines = file.readlines()

for line in lines:
    words = line.replace('!', ' ').replace('?', ' ').replace('.', ' ').replace(',', ' ').split()
    for word in words:
        if word in frequency:
            frequency[word] += 1
        else:
            frequency[word] = 1

frequency = dict(sorted(frequency.items(), reverse=True, key=lambda kvp: kvp[1]))

with open("results.txt", 'w') as file:
    for kvp in frequency.items():
        file.write(f"{kvp[0]}:{kvp[1]}\n")