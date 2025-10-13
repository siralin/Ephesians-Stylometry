from collections import Counter
from statistics import stdev, fmean
from unit_frequency_utils import unit_counts_to_normalized_frequencies

# Returns a tuple of a 2d array and a list of words
# where array[book index][word index] = zscore
# and the book index matches the index of the same book in the given book_to_word_counts
# and the word index matches the index of the same word in the returned list of words.
#
# book_to_text: Dict of book title to all the text in that book, appropriately normalized.  May or may not contain whitespace.
# num_words: int, the number of most common words the frequencies should be calculated for
# normalization_method: whether to normalize frequencies by 'zscore' or 'simple' method
def calculate_normalized_word_frequencies(book_to_text, num_words, normalization_method):
  return unit_counts_to_normalized_frequencies(
    num_words, count_words_per_book(book_to_text), count_words_overall(book_to_text), normalization_method)

# Returns a list of Counters, one per book,
# counting the number of times each word appears in the book.
def count_words_per_book(book_to_text):
  book_to_word_counts = [None] * len(book_to_text)
  for index, book in enumerate(book_to_text):
    words = book_to_text[book].split(' ')
    book_to_word_counts[index] = Counter(words)
  return book_to_word_counts

# Returns a Counter containing the number of times each word appears in the whole corpus.
def count_words_overall(book_to_text):
  overall_word_counts = Counter()
  for index, book in enumerate(book_to_text):
    words = book_to_text[book].split(' ')
    overall_word_counts.update(words)
  return overall_word_counts
