import csv
with open('data.csv', newline='') as csvfile:
    csvreader = csv.DictReader(csvfile, fieldnames=['date', 'rainfall_mm', 'temperature_c', 'landslide'])
    
    for row in csvreader:
        # print(', '.join(row.values()))
        print(row)    