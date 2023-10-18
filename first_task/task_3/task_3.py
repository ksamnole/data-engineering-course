variant = 25

with open("text_3_var_25") as file:
    lines = file.readlines()

with open("results.txt", 'w') as file:
    for line in lines:
        numbers = line.split(',')
        for i in range(len(numbers) - 1):
            if numbers[i].isdigit():
                number = int(numbers[i])
            else:
                number = (int(numbers[i - 1]) + int(numbers[i + 1])) / 2
            if number ** 0.5 >= 50 + variant:
                file.write(f"{int(number)}\n")