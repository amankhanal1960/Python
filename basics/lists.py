# lists : ordered, mutable, allows duplicate elements
mylist = ["banana", "apple", "cherry"]
print("\n", mylist)

item = mylist[2]
# print(item) 

for i in mylist:
    print(i)
    
    

# listcopy just points to the same list as mylist, so any changes made to listcopy will also affect mylist.
listcopy = mylist
listcopy.append("mango")
print(listcopy)
print(mylist)

# This wont affect mylist as listcopy is a copy of mylist and not pointing to the same list.
listcopy = list(mylist)
listcopy.append("mango")
print(listcopy)
print(mylist)

# This also wont affect mylist as listcopy is a copy of mylist and not pointing to the same list.
listcopy = mylist.copy()
listcopy.append("mango")
print(listcopy)
print(mylist)

# This also wont affect mylist as listcopy is a copy of mylist and not pointing to the same list.
listcopy = mylist[:]
listcopy.append("mango")
print(listcopy)
print(mylist)

