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

file_path = Path(__file__).resolve().parent

data_file = file_path / "data.txt"

my_string = data_file.read_text()

string_lower = my_string.lower()

table = str.maketrans("", "", string.punctuation)

clean_str = string_lower.translate(table)

words_list = clean_str.split()

word_counts = Counter(words_list)

top_10_words = word_counts.most_common(10)

for word, count in top_10_words:
    print(f"{word}:{count}")