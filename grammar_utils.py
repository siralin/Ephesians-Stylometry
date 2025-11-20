from collections import Counter
from statistics import stdev, fmean
from unit_frequency_utils import unit_counts_to_normalized_frequencies, unit_counts_to_raw_frequencies

# Returns a tuple of a 2d array and a list of ngrams
# where array[book index][ngram index] = zscore
# and the book index matches the index of the same book in the given book_to_ngram_counts
# and the ngram index matches the index of the same ngram in the returned list of ngrams.
#
# book_to_text: Dict of book title to the parts of speech of all the text in that book.
# num_ngrams: int, the number of most common ngrams the frequencies should be calculated for
# normalization_method: whether to normalize frequencies by 'zscore' or 'simple' method
def calculate_normalized_part_of_speech_ngram_frequencies(book_to_text, num_ngrams, ngram_size, normalization_method):
  book_to_ngram_counts, overall_ngram_counts = _count_ngrams(book_to_text, ngram_size)

  return unit_counts_to_normalized_frequencies(
    num_ngrams, book_to_ngram_counts, overall_ngram_counts, normalization_method)

# Returns a tuple where the left is a list of Counters, one for each book,
# containing the number of times each part-of-speech ngram occurs in the book, and the right is a Counter
# containing the number of times each part-of-speech ngram occurs in every book.
def _count_ngrams(book_to_text, ngram_size):
  # This is a list of Counters, one for each book
  book_to_ngram_counts = [None] * len(book_to_text)
  overall_ngram_counts = Counter()

  for index, book in enumerate(book_to_text):
    parts = book_to_text[book].split(' ')
    book_to_ngram_counts[index] = Counter()
    for i in range(0, len(parts) - ngram_size + 1):
      ngram = ' '.join(parts[i:i + ngram_size])

      book_to_ngram_counts[index][ngram] += 1
      overall_ngram_counts[ngram] += 1

  return book_to_ngram_counts, overall_ngram_counts

# Returns the relative frequencies of the given parts of speech
# (as a fraction of the total words in each book)
# in the form of a 2d List[book][word]
def calculate_raw_part_of_speech_frequencies(book_to_text, num_ngrams, ngram_size):
  book_to_ngram_counts, overall_ngram_counts = _count_ngrams(book_to_text, ngram_size)

  return unit_counts_to_raw_frequencies(num_ngrams, book_to_ngram_counts, overall_ngram_counts)
