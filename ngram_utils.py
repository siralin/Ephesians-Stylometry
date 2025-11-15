from collections import Counter
from statistics import stdev, fmean
from unit_frequency_utils import unit_counts_to_normalized_frequencies

# Returns a tuple of a 2d array and a list of ngrams
# where array[book index][ngram index] = zscore
# and the book index matches the index of the same book in the given book_to_ngram_counts
# and the ngram index matches the index of the same ngram in the returned list of ngrams.
#
# book_to_text: Dict of book title to all the text in that book, appropriately normalized.  May or may not contain whitespace.
# num_ngrams: int, the number of most common ngrams the frequencies should be calculated for
# normalization_method: whether to normalize frequencies by 'zscore' or 'simple' method
def calculate_normalized_ngram_frequencies(book_to_text, num_ngrams, ngram_size, normalization_method):
  # first, calculate frequency of every possible ngram in each book.
  # This is a list of Counters, one for each ngram
  book_to_ngram_counts = [None] * len(book_to_text)
  overall_ngram_counts = Counter()

  for index, book in enumerate(book_to_text):
    text = book_to_text[book]
    book_to_ngram_counts[index] = Counter()
    for i in range(0, len(text) - ngram_size + 1):
      ngram = text[i:i + ngram_size]

      # can remove ngrams containing spaces if you want
      #if " " not in ngram:
      book_to_ngram_counts[index][ngram] += 1
      overall_ngram_counts[ngram] += 1

  return unit_counts_to_normalized_frequencies(
    num_ngrams, book_to_ngram_counts, overall_ngram_counts, normalization_method)
