avg = []

with open("text_2_var_25") as file:
    lines = file.readlines()

for line in lines:
    numbers = list(map(int, line.split()))
    s = sum(numbers)
    count = len(numbers)
    avg.append(s/count)

with open("results.txt", 'w') as file:
    for res in avg:
        file.write(f"{res}\n")