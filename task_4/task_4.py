import csv

filter = 25 + (25 % 10)

with open('text_4_var_25', 'rt', encoding='utf-8') as csvfile:
    csv_reader = csv.reader(csvfile, delimiter=',')
    with open('result', 'w', encoding='utf-8') as res_csv:
        csv_writer = csv.writer(res_csv)
        for row in csv_reader:
            csv_writer.writerow((row[0], row[1], row[2], row[3], row[4]))
