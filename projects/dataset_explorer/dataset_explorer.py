import csv

rows = []
with open('data.csv', newline='') as csvfile:
    csvreader = csv.DictReader(csvfile)
    
    for row in csvreader:  
        rows.append(row)
    
    headers = csvreader.fieldnames
    
    for item in headers:
        missing_count = 0
        for index, row in enumerate(rows, start=1):
            if row[item] == '':
                missing_count += 1
                print(f"Missing item in row {index} is {item}")      
        print(f"Total missing percentage in column {item} is: {missing_count / len(rows) * 100}%")
        
