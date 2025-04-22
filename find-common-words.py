import os
from collections import Counter

directory = 'netbible_chapters'

book_to_word_counts = {}
total_word_counts = Counter()

for filename in os.listdir(directory):
  if '-norm' in filename:
    book = filename[:filename.index('-')]
    if book not in book_to_word_counts:
      book_to_word_counts[book] = Counter()

    with open(os.path.join(directory, filename), 'r') as handle:
      for line in handle:
        words = line.split()
        for word in words:
          book_to_word_counts[book][word] += 1
          total_word_counts[word] += 1
print(total_word_counts.most_common(50))
for book in book_to_word_counts.keys():
  print(book)
  print(book_to_word_counts[book].most_common(50))