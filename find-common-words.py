from collections import Counter
from delta_utils import read_in_book_to_word_counts

book_to_word_counts = read_in_book_to_word_counts()
total_word_counts = Counter()
for _, word_counts in book_to_word_counts.items():
  total_word_counts.update(word_counts)

print([x[0] for x in total_word_counts.most_common(100)])

#for book in book_to_word_counts.keys():
#  print(book)
#  print(book_to_word_counts[book].most_common(50))