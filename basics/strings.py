# String concatenation

greeting = "Hello"
name = "Aman"

# Concat
message = greeting + " " + name + "!"
print(message)
# this outputs Hello Aman!

# Multiplier
cheer = "Horray " * 3 + "!!"
print(cheer)

# indexing and slicing 

text = "Aman is a good boy!"
print(text[0:4]) # Aman
print(text[5:7]) # is                           
print(text[8:9])  # a                                      
print(text[10:14])  # good                                      
print(text[15:19])   # boy!                                     

print(text[-5:-1]) # boy
print(text[10:])    # prints everything after the index 10
print(text[:4])   # prints everything before the index 4

# reversing a string
print(text[::-1])

# built in functions

# strip() - removes leading and trailing whitespaces
dirty_input = "              aman is a bad boy  "
clean_input = dirty_input.strip()
print(clean_input)

#.split - break the sentence into words using .split()

fruits = "apple orange banana pineapple mango guava"
word = fruits.split()
print(word)
fruits = "apple, orange, banana, pineapple, mango, guava"
words = fruits.split(",")
print(words)

# join() - get those words together
joined = "_".join(word)
print(joined)
