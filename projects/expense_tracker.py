expenses = [["1", "250", "Food", "2023-06-01"], ["2", "1200", "Transport", "2023-06-02"], ["3", "150", "Entertainment", "2023-06-03"],["2", "550", "Food", "2023-06-04"]]
expense_dict = [{"id": int(item[0]), "amount": float(item[1]), "category": item[2], "date": item[3]} 
                for item in expenses]   

print(expense_dict)

print(expense_dict[1]["category"]) 

print("Total Expense is: ",sum(item["amount"] for item in expense_dict))
# print("Total Price is: ", sum(float(item[1]) for item in Expenses))

summary_dict = {}
for item in expense_dict:
    
    if item["category"] in summary_dict:
        summary_dict[item["category"]]["amount"] += item["amount"]
    else:
        summary_dict[item["category"]] = {"amount":item["amount"]}
    
print(summary_dict["Food"])

