from collections import Counter
from statistics import stdev, fmean
from unit_frequency_utils import unit_counts_to_normalized_frequencies

# Returns a tuple of a 2d array and a list of ngrams
# where array[book index][ngram index] = zscore
# and the book index matches the index of the same book in the given book_to_ngram_counts
# and the ngram index matches the index of the same ngram in the returned list of ngrams.
#
# book_to_text: Dict of book title to the parts of speech of all the text in that book.
# min_count: int, the min count for the most common ngrams the frequencies should be calculated for
# normalization_method: whether to normalize frequencies by 'zscore' or 'simple' method
def calculate_normalized_part_of_speech_ngram_frequencies(book_to_text, min_count, ngram_size, normalization_method):
  # first, calculate frequency of every possible ngram in each book.
  # This is a list of Counters, one for each ngram
  book_to_ngram_counts = [None] * len(book_to_text)
  overall_ngram_counts = Counter()

  for index, book in enumerate(book_to_text):
    parts = book_to_text[book].split(' ')
    book_to_ngram_counts[index] = Counter()
    for i in range(0, len(parts) - ngram_size + 1):
      ngram = ' '.join(parts[i:i + ngram_size])

      book_to_ngram_counts[index][ngram] += 1
      overall_ngram_counts[ngram] += 1

  return unit_counts_to_normalized_frequencies(
    min_count, book_to_ngram_counts, overall_ngram_counts, normalization_method)
