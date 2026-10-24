import csv
import argparse

def load_dataset(filepath):
    rows = []
    with open(filepath, newline='') as csvfile:
        csvreader = csv.DictReader(csvfile)
        
        for row in csvreader:  
            rows.append(row)
        headers = csvreader.fieldnames
    return rows, headers
    

def find_missing(rows, headers):
    for item in headers:
        missing_count = 0
        for index, row in enumerate(rows, start=1):
            if row[item] == '':
                missing_count += 1
                print(f"Missing item in row {index} is {item}")      
        # print(f"Total missing percentage in column {item} is: {missing_count / len(rows) * 100}%")
def find_stats(rows):  
    rainfall_sum = 0
    temperature_sum = 0
    rainfall_count = 0
    temperature_count = 0 
    temperature_max, rainfall_max = float('-inf'), float('-inf')
    temperature_min, rainfall_min = float('inf'), float('inf')
    for row in rows:
            if row['rainfall_mm']:
                if row['rainfall_mm'] != '':
                    current_rainfall = float(row['rainfall_mm'])
                    rainfall_sum += float(row['rainfall_mm'])
                    rainfall_count += 1
                    rainfall_max = max(rainfall_max, current_rainfall)
                    rainfall_min = min(rainfall_min, current_rainfall)
            if row['temperature_c']:
                if row['temperature_c'] != '':
                    current_temperature = float(row['temperature_c'])
                    temperature_sum += float(row['temperature_c'])
                    temperature_count += 1
                    temperature_max = max(temperature_max, current_temperature)
                    temperature_min = min(temperature_min, current_temperature)
                    
    print(f"The sum is for rainfall is: {rainfall_sum}")
    print(f"The sum is for temperature is: {temperature_sum}")
    print(f"The maximum temperature is: {temperature_max}")
    print(f"The minimum temperature is: {temperature_min}")
    print(f"The maximum rainfall is: {rainfall_max}")
    print(f"The minimum rainfall is: {rainfall_min}")
    print(f"Mean temperature is: {temperature_sum/ temperature_count}")
    print(f"Mean Rainfall is: {rainfall_sum/ rainfall_count}")
    
def inspect(rows, headers): 
    num_rows = len(rows)
    num_column = len(headers)
    print(f"Number of rows are: {num_rows}")
    print(f"Number of columns are: {num_column}")
    
    for item in headers:
        nan_count = 0   
        for row in rows:
            if row[item] == '':
                nan_count += 1
        print(f"NAN count for row {item} is : {nan_count}")
        
def main():
    parser = argparse.ArgumentParser(
        description="dataset explorer CLI"
    )    

    parser.add_argument(
        "command",
        choices=["inspect", "stats", "missing"],
        help="Command to execute"
    )
    
    parser.add_argument(
        "filepath",
        help="Path to the csv file"
    )

    args = parser.parse_args()
    
    rows, headers = load_dataset(args.filepath)
    
    if args.command == "inspect":
        inspect(rows, headers)
    elif args.command == "stats":
        find_stats(rows)
    elif args.command == "missing":
        find_missing(rows, headers)
    else:
        print("Error: Something went wrong!")
        
if __name__ == "__main__":
    main()