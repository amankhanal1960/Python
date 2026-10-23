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
        
    rainfall_sum = 0
    temperature_sum = 0
    temperature_max, rainfall_max = float('-inf'), float('-inf')
    temperature_min, rainfall_min = float('inf'), float('inf')
    for row in rows:
            if row['rainfall_mm']:
                if row['rainfall_mm'] != '':
                    current_rainfall = float(row['rainfall_mm'])
                    rainfall_sum += float(row['rainfall_mm'])
                    rainfall_max = max(rainfall_max, current_rainfall)
                    rainfall_min = min(rainfall_min, current_rainfall)
            if row['temperature_c']:
                if row['temperature_c'] != '':
                    current_temperature = float(row['temperature_c'])
                    temperature_sum += float(row['temperature_c'])
                    temperature_max = max(temperature_max, current_temperature)
                    temperature_min = min(temperature_min, current_temperature)
                    
    print(f"The sum is for rainfall is: {rainfall_sum}")
    print(f"The sum is for temperature is: {temperature_sum}")
    print(f"The maximum temperature is: {temperature_max}")
    print(f"The minimum temperature is: {temperature_min}")
    print(f"The maximum rainfall is: {rainfall_max}")
    print(f"The minimum rainfall is: {rainfall_min}")
    
    
    
    
    
    
    
    # for row in rows:
    #     if row['temperature_c']:
    #         if row['temperature_c'] != '':
    #             temperature_sum += float(row['temperature_c'])
                