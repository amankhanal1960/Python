mydict = {"name" : "aman", "age" : 20, "gender" : "male"}
print(mydict)

mydict2 = dict(name = "aman", age = 20, gender = "male")
print(mydict2)

value = mydict["name"]
print(value)

# we can add new key value pair also
mydict["job"] = "Student"
print(mydict)

# we can remove the pair using del or pop method

del mydict["job"]
print(mydict)

mydict.pop("name")
print(mydict)

# similarly we can see if we have a key in the dictionary or not

if "name" in mydict:
    print("name is there")
else:
    print("name is not there")
    
try:
    print(mydict["name"])
except KeyError:
    print("name is not there")
    
    
for x in mydict.keys():
    print(x)

for x in mydict.values():
    print(x)
    
for key, value in mydict.items():
    print(key, value)