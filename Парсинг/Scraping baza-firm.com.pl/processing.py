import csv
emails = []
with open("all_firms.csv", newline='', encoding='utf-8') as file:
    reader = csv.reader(file, delimiter=';')
    for row in reader:
        if row[3] not in emails:
            with open("result_firms.csv", 'a', newline='', encoding='utf-8') as f:
                writer = csv.writer(f, delimiter=';')
                writer.writerow(row)
                if row[3] != 'None':
                    emails.append(row[3])
