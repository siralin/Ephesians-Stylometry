from collections import Counter
from statistics import stdev, fmean

# Returns a tuple of a 2d array and a list of ngrams
# where array[book index][ngram index] = zscore
# and the book index matches the index of the same book in the given book_to_ngram_counts
# and the ngram index matches the index of the same ngram in the returned list of ngrams.
#
# num_ngrams: int, the number of most common ngrams the zscores should be calculated for
# book_to_ngram_counts: List<Counter>, the number of times every ngram appears in each book
# overall_ngram_counts: Counter, the number of times every ngram appears in all books
def ngram_counts_to_normalized_frequencies(num_ngrams, book_to_ngram_counts, overall_ngram_counts, normalization_method):

  # List of up to num_ngrams ngrams that appear the most frequently overall.
  most_frequent_ngrams = [x[0] for x in overall_ngram_counts.most_common(num_ngrams)]

  # 2d List of book to ngram to frequency
  # where the book indexes match those in book_to_ngram_counts
  # and the ngram indexes match those in most_frequent_ngrams
  book_to_ngram_frequencies = _find_book_to_ngram_frequencies(book_to_ngram_counts, most_frequent_ngrams)

  book_to_normalized_ngram_frequency = _normalize_frequencies(book_to_ngram_frequencies, normalization_method)
  return (book_to_normalized_ngram_frequency, most_frequent_ngrams)

# Returns the relative frequencies of the given ngrams
# (as a fraction of the total ngrams in each book)
# in the form of a 2d List[book][ngram]
#
# book_to_ngram_counts: List<Counter>, the number of times every ngram appears in each book
# ngrams: List of ngrams we're interested in
def _find_book_to_ngram_frequencies(book_to_ngram_counts, ngrams):
  num_books = len(book_to_ngram_counts)
  num_ngrams = len(ngrams)

  book_to_ngram_frequencies = [None] * num_books
  for book_index, ngram_counts in enumerate(book_to_ngram_counts):
    total_ngrams = sum(ngram_counts.values()) # Counter.total() not added till 3.10
    book_to_ngram_frequencies[book_index] = [0] * num_ngrams
    for ngram_index, ngram in enumerate(ngrams):
      book_to_ngram_frequencies[book_index][ngram_index] = ngram_counts[ngram] / total_ngrams

  return book_to_ngram_frequencies

# Normalizes the given relative frequencies using the given method.
#
# book_to_ngram_frequencies: 2d List of book to ngram to frequency
# normalization_method: String.  If 'zscore', then for each ngram the results will have a mean of 0 and std dev of 1.
#   If 'simple', then for each ngram the results will be scaled to have a minimum of -1 and a maximum of 1.
def _normalize_frequencies(book_to_ngram_frequencies, normalization_method):
  if normalization_method == 'zscore':
    return _normalize_frequencies_to_zscore(book_to_ngram_frequencies)
  elif normalization_method == 'simple':
    pass # TODO implement
  else:
    raise ValueError(normalization_method)

# Normalizes the given relative frequencies to zscores.
# For each ngram the results will have a mean of 0 and std dev of 1.
#
# book_to_ngram_frequencies: 2d List of book to ngram to frequency
def _normalize_frequencies_to_zscore(book_to_ngram_frequencies):
  # Invert the 2d List.
  # Need to convert the Zip to a List so that it can be iterated twice.
  ngram_to_book_to_frequencies = list(zip(*book_to_ngram_frequencies))

  means = [fmean(frequencies) for frequencies in ngram_to_book_to_frequencies]
  std_devs = [stdev(frequencies) for frequencies in ngram_to_book_to_frequencies]

  book_to_ngram_zscores = [None] * len(book_to_ngram_frequencies)
  for book_index, ngram_frequencies in enumerate(book_to_ngram_frequencies):
    book_to_ngram_zscores[book_index] = [(freq - means[ngram_index]) / std_devs[ngram_index] for ngram_index, freq in enumerate(ngram_frequencies)]

  return book_to_ngram_zscores
