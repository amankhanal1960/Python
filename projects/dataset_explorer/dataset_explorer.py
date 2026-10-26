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
    

def find_missing_summary(rows, headers):
    for item in headers:
        missing_rows = []
        
        for index, row in enumerate(rows, start=1):
            if row[item] == '':
                missing_rows.append(index)
        if len(missing_rows) > 0:
            count = len(missing_rows)
            print(f"Column {item} is missing {count} item in row {missing_rows}")

def find_stats(rows, headers):  
    stats = {}
    for row in rows:
        for item in headers:
            try:
                row[item] = float(row[item]) 
                
                if item not in stats:
                    stats[item] = {
                        'sum': 0.0,
                        'count': 0,
                        'max': float('-inf'),
                        'min': float('inf')
                    } 
                stats[item]['sum'] += row[item]
                stats[item]['count'] += 1
                stats[item]['max'] = max(stats[item]['max'], row[item])
                stats[item]['min'] = min(stats[item]['min'], row[item])
                
            except ValueError:
                pass

    print(f"{'Column Name':<20}{'Mean':<12}{'Min':<12}{'Max':<12}")
    print("-" * 51)
        
    for key, value in stats.items():
        if value['count'] == 0:
            print(f"{key:<20}{'N/A':<12}{'N/A':<12}{'N/A':<12}")
            continue
        
        mean_value = value['sum'] / value['count']
        mean_val = round(mean_value, 2)
        max_val = round(value['max'], 2)
        min_val = round(value['min'], 2)
        
        print(f"{key:<20}{mean_val:<12}{max_val:<12}{min_val:<12}")
 
def inspect(rows, headers): 
    sample_rows = rows[:5]
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
  
    for header in headers:
        print(header, end="\t")
    print()
    print("--------------------------------------")
    
    for row in sample_rows:
        for header in headers:
            print(row[header], end="\t")
        print()
        
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
        find_stats(rows, headers)
    elif args.command == "missing":
        find_missing_summary(rows, headers)
    else:
        print("Error: Something went wrong!")
        
if __name__ == "__main__":
    main()