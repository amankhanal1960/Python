mytuple = ("banana", "apple", "cherry")
print(mytuple)
print(type(mytuple))

mituple = tuple(["banana", "apple", "cherry"])
print(mituple)

for i in mytuple:
    print(i)
    
if "apple" in mytuple:
    print("Yes, 'apple' is in the tuple")
else:
    print("No its not in the tuple")
    
yourtuple = ('a', 'b', 'c', 'd', 'e', 'a', 'b', 'c', 'd', 'e')
print(len(yourtuple))
print(yourtuple.count("a"))

# we can convert the tuple into list

mylist = list(mytuple)

# similarly we can convert the list back to tuple

mytuple2 = tuple(mylist)

# this will print the elements from index 1 to 8 with a step of 3
print(yourtuple[1:8:3])

# -1 step reverses the tuple
print(yourtuple[::-1])

# creating a tuple and assigning it to a variable
tpl = "john", "30", "male"

name, age, sex = tpl

print(name)
print(age)
print(sex)