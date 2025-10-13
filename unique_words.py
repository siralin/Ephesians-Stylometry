from read_text_utils import read_normalized_texts
from word_utils import count_words_overall, count_words_per_book

book_to_text = read_normalized_texts()
overall_word_counts = count_words_overall(book_to_text)
book_word_counts = count_words_per_book(book_to_text)

for book, word_counts in zip(book_to_text.keys(), book_word_counts):
  unique_words_in_book = 0 # number of unique words used in no other books
  unique_word_count_in_book = 0 # number of times unique words used in this book
  total_words_in_book = 0
  for word, book_count in word_counts.items():
    total_words_in_book += book_count
    if overall_word_counts[word] == book_count:
      unique_words_in_book += 1
      unique_word_count_in_book += book_count
  print(','.join([book, str(unique_words_in_book), str(unique_word_count_in_book), str(total_words_in_book)]))

# TODO what if we combine colossians and ephesians?