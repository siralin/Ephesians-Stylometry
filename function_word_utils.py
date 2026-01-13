from collections import Counter
from statistics import stdev, fmean
from unit_frequency_utils import unit_counts_to_normalized_frequencies_for_given_units, _find_book_to_unit_frequencies

# Returns a tuple of a 2d array and a list of words
# where array[book index][word index] = zscore
# and the book index matches the index of the same book in the given book_to_word_counts
# and the word index matches the index of the same word in the returned list of words.
#
# book_to_text: Dict of book title to all the text in that book, appropriately normalized.  May or may not contain whitespace.
# function_words: int, the words the frequencies should be calculated for
# normalization_method: whether to normalize frequencies by 'zscore' or 'simple' method
def calculate_normalized_function_word_frequencies(book_to_text, function_words, normalization_method):
  # first, calculate frequency of every possible word in each book.
  # This is a list of Counters, one for each word
  book_to_word_counts = [None] * len(book_to_text)

  for index, book in enumerate(book_to_text):
    words = book_to_text[book].split(' ')
    book_to_word_counts[index] = Counter(words)

  return unit_counts_to_normalized_frequencies_for_given_units(
    function_words, book_to_word_counts, normalization_method)

# Returns the relative frequencies of the given words
# (as a fraction of the total words in each book)
# in the form of a 2d List[book][word]
def calculate_raw_function_word_frequencies(book_to_text, function_words):
  # This is a list of Counters, one for each word
  book_to_word_counts = [None] * len(book_to_text)

  for index, book in enumerate(book_to_text):
    words = book_to_text[book].split(' ')
    book_to_word_counts[index] = Counter(words)

  return _find_book_to_unit_frequencies(book_to_word_counts, function_words)
