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
  # first, calculate frequency of every possible word in each book.
  # This is a list of Counters, one for each word
  book_to_word_counts = [None] * len(book_to_text)
  overall_word_counts = Counter()

  for index, book in enumerate(book_to_text):
    words = book_to_text[book].split(' ')
    book_to_word_counts[index] = Counter(words)
    overall_word_counts.update(words)

  return unit_counts_to_normalized_frequencies(
    num_words, book_to_word_counts, overall_word_counts, normalization_method)
