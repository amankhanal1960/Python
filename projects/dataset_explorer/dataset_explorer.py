import csv

rows = []
with open('data.csv', newline='') as csvfile:
    csvreader = csv.DictReader(csvfile)
    
    for row in csvreader:  
        rows.append(row)
    
    headers = csvreader.fieldnames
    
    missing_count = 0
    missing_found = False
    for row in rows:
        for item in row:
            if row[item] == '':
                missing_found = True
                missing_count += 1
    if missing_found:
         print(f"Missing item is {item}")      
    print(f"Total missing percentage is: {missing_count / len(rows) * 100}%")