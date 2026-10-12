# Get the file path
# Open and read the whole file into a string
# Convert everything to lowercase
# Remove the punctuations
# Split the test into list of words
# Count how namy times each word appears
# Sort the counts from highest to lowest
# Print the top 10

from collections import Counter
from pathlib import Path
import string

# Get the file path from the current file
file_path = Path(__file__).resolve().parent

# Get the data file path
data_file = file_path / "data.txt"

#Read the file into a string
my_string = data_file.read_text()

# convert everything to lowercase
string_lower = my_string.lower()

# Remove the punctuations by creating a translation table and using the translate method
table = str.maketrans("", "", string.punctuation)
clean_str = string_lower.translate(table)

# Split the whole text into a list of words
words_list = clean_str.split()

# Count how many times each words have been repeated in the word list 
word_counts = Counter(words_list)

# Sort the counts from highest to lowest and get the top 10 words
top_10_words = word_counts.most_common(10)

for word, count in top_10_words:
    print(f"{word}:{count}")