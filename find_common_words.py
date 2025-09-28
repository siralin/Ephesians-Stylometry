from collections import Counter
from read_text_utils import read_normalized_texts

book_to_text = read_normalized_texts()

total_word_counts = Counter()
for text in book_to_text.values():
  total_word_counts.update(text.split(' '))

print([x[0] for x in total_word_counts.most_common(100)])