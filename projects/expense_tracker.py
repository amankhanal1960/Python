import argparse

expenses = [["1", "250", "Food", "2023-06-01"], ["2", "1200", "Transport", "2023-06-02"], ["3", "150", "Entertainment", "2023-06-03"],["4", "550", "Food", "2023-06-04"]]
expense_dict = [{"id": int(item[0]), "amount": float(item[1]), "category": item[2], "date": item[3]} 
                for item in expenses]   

# print(expense_dict)

# print(expense_dict[1]["category"])

# print("Total Expense is: ",sum(item["amount"] for item in expense_dict))
# print("Total Price is: ", sum(float(item[1]) for item in Expenses))

def summary():
    summary_dict = {}
    for item in expense_dict:
        
        if item["category"] in summary_dict:
            summary_dict[item["category"]] += item["amount"]
        else:
            summary_dict[item["category"]] = item["amount"]

    # for key, value in summary_dict.items():
    #     print(f" {key}, NPR {value}")
        
    return summary_dict

def list_expenses():
    for item in expense_dict:
        
        print( f"'id': {item["id"]}, 'amount': {item["amount"]}, 'category': {item["category"]}, 'date': {item["date"]}")
        
def filter_expenses_by_category(category):
    category_found = False
    for item in expense_dict:
        if item["category"].lower() == category.lower():
            print(f" 'id': {item["id"]}, 'amount': {item["amount"]}, 'category': {item["category"]} ")
            category_found = True
    if not category_found:
        print(f"Not existing category: {category}")
            

def add_expense():
    # Implementation for adding an expense
    pass

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
            "category", 
            nargs="?",
            help="Category to filter expenses by"
        )
    
    args = parser.parse_args()
    
    if args.command == "summary":
        summary()
    elif args.command == None:
        parser.print_help()
    elif args.command == "list":
        list_expenses()
    elif args.command == "filter" and args.category:
        filter_expenses_by_category(args.category)
    else:
        parser.error(f"Unknown command: {args.command}")
        
    if args.command == "add":
        add_expense()
    
        
if __name__ == "__main__":
    main()
