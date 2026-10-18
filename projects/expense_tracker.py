import argparse
from datetime import date
from pathlib import Path
import json

# expenses = [["1", "250", "Food", "2023-06-01"], ["2", "1200", "Transport", "2023-06-02"], ["3", "150", "Entertainment", "2023-06-03"],["4", "550", "Food", "2023-06-04"]]
# expense_dict = [{"id": int(item[0]), "amount": float(item[1]), "category": item[2], "date": item[3]} 
#                 for item in expenses]   

# print(expense_dict)

# print(expense_dict[1]["category"])

# print("Total Expense is: ",sum(item["amount"] for item in expense_dict))
# print("Total Price is: ", sum(float(item[1]) for item in Expenses))

file_path = Path(__file__).resolve().parent
data_file = file_path / "data.json"
try:
    my_string = data_file.read_text()
    expenses = json.loads(my_string)
    expense_dict = expenses
    
except OSError as e:
    print(f"Error reading the file: {e}")
    exit()
    

def summary():
    summary_dict = {}
    for item in expense_dict:
        
        if item["category"] in summary_dict:
            summary_dict[item["category"]] += item["amount"]
        else:
            summary_dict[item["category"]] = item["amount"]

    for key, value in summary_dict.items():
        print(f" {key}, NPR {value}")
        
    return summary_dict

def list_expenses():
    for item in expense_dict:
        
        print( f"'id': {item['id']}, 'amount': {item['amount']}, 'category': {item['category']}, 'date': {item['date']}")
        
def filter_expenses_by_category(category):
    category_found = False
    for item in expense_dict:
        if item["category"].lower() == category.lower():
            print(f" 'id': {item["id"]}, 'amount': {item["amount"]}, 'category': {item["category"]} ")
            category_found = True
    if not category_found:
        print(f"No existing category: {category}")
            

def add_expense(amount, category, note):
    new_id = len(expenses) + 1
    
    new_expense = {
        "id": new_id,
        "amount": int(amount), 
        "category": category,
        "note": note,
        "date": date.today()
        
    }
    try:
        # add the new expense using standard .append()
        expenses.append(new_expense)
        # convert the updated list back into a json string
        updated_string = json.dumps(expenses, indent=4)
        # write it back to the file
        data_file.write_text(updated_string)
        
        print("successfully added the new expense.")
    except OSError as e:
        print(f"File error: {e}")

def main():
    parser = argparse.ArgumentParser(
        description="Expense tracker CLI"
    )
    
    parser.add_argument(
        "command", 
        nargs="?",
        help="Command to execute: summary, add, remove, list"
    )
    
    parser.add_argument(
        "--category", 
        help="Enther the category"
    )
    parser.add_argument(
            "--amount",
            help=" Enter the amount"
        )

    parser.add_argument(
            "--note",
            help=" Enter the a note"
        )

    args = parser.parse_args()
    
    if args.command == "summary":
        summary()
    elif args.command == None:
        parser.print_help()
    elif args.command == "list" and args.category:
        filter_expenses_by_category(args.category)
    elif args.command == "list":
        list_expenses()
    elif args.command == "add":
        if args.amount and args.category:
            add_expense(args.amount, args.category, args.note)
        else:
            print("Error: 'add' requires both --amount and --category")
            
    else:
        print("Something went wrong")
    
        
if __name__ == "__main__":
    main()
