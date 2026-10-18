# Get the file path
# Open and read the whole file into a string
# Convert everything to lowercase
# Remove the punctuations
# Split the test into list of words
# Count how namy times each word appears
# Sort the counts from highest to lowest
# Print the top 10

from pathlib import Path
import string

try:
    # Get the file path from the current file
    file_path = Path(__file__).resolve().parent

    # Get the data file path
    data_file = file_path / "data.txt"

    #Read the file into a string
    my_string = data_file.read_text()
except OSError as e:
    print(f"Error reading the file: {e}")
    exit(1)

# convert everything to lowercase
string_lower = my_string.lower()

# Remove the punctuations by creating a translation table and using the translate method
table = str.maketrans("", "", string.punctuation)
clean_str = string_lower.translate(table)

# Split the whole text into a list of words
words_list = clean_str.split()

# Count how many times each words have been repeated in the word list 
words_count = {}
for word in words_list:
    if word in words_count:
        words_count[word] += 1
    else:
        words_count[word] = 1
        
# Sort the counts from highest to lowest and get the top 10 words
top_10_words = sorted(words_count.items(), key=lambda x: x[1], reverse=True)[:10]

for word, count in top_10_words:
    print(f"{word}:{count}")
    
if words_count == {}:
    print("The file is empty or contains no valid words.")