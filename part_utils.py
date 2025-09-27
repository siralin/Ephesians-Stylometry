from collections import Counter
from statistics import stdev, fmean
from unit_frequency_utils import unit_counts_to_normalized_frequencies

# Returns a tuple of a 2d array and a list of parts
# where array[book index][part index] = zscore
# and the book index matches the index of the same book in the given book_to_part_counts
# and the part index matches the index of the same part in the returned list of parts.
#
# book_to_text: Dict of book title to all the text in that book, appropriately normalized.  May or may not contain whitespace.
# num_parts: int, the number of most common parts of speech the frequencies should be calculated for
# normalization_method: whether to normalize frequencies by 'zscore' or 'simple' method
def calculate_normalized_part_frequencies(book_to_text, num_parts, normalization_method):
  # first, calculate frequency of every possible part in each book.
  # This is a list of Counters, one for each part
  book_to_part_counts = [None] * len(book_to_text)
  overall_part_counts = Counter()

  for index, book in enumerate(book_to_text):
    parts = book_to_text[book].split(' ')
    book_to_part_counts[index] = Counter(parts)
    overall_part_counts.update(parts)

  return unit_counts_to_normalized_frequencies(
    num_parts, book_to_part_counts, overall_part_counts, normalization_method)
