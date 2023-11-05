import csv

age_filter = 25 + (25 % 10)

with open('text_4_var_25', 'rt', encoding='utf-8') as csvfile:
    csv_reader = csv.reader(csvfile, delimiter=',')
    with open('result', 'w', encoding='utf-8') as res_csv:
        csv_writer = csv.writer(res_csv)
        summa = 0
        count = 0
        data = []
        for row in csv_reader:
            summa += int(row[4][:-1])
            count += 1
            data.append((row[0], row[1], row[2], row[3], row[4]))
        avg_sum = summa / count
        data.sort(key=lambda x: x[0])
        for doc in data:
            if int(doc[4][:-1]) >= avg_sum and int(doc[0]) > age_filter:
                csv_writer.writerow(doc)
