from collections import Counter
from statistics import stdev, fmean

# Returns a tuple of a 2d array and a list of units (strings)
# where array[book index][unit index] = zscore
# and the book index matches the index of the same book in the given book_to_unit_counts
# and the unit index matches the index of the same unit in the returned list of units.
#
# num_units: int, the number of most common units the frequencies should be calculated for
# book_to_unit_counts: List<Counter>, the number of times every unit appears in each book
# overall_unit_counts: Counter, the number of times every unit appears in all books
def unit_counts_to_normalized_frequencies(num_units, book_to_unit_counts, overall_unit_counts, normalization_method):

  # List of up to num_units units that appear the most frequently overall.
  most_frequent_units_and_counts = overall_unit_counts.most_common(num_units)
  most_frequent_units = [x[0] for x in most_frequent_units_and_counts]

  total_count = sum(overall_unit_counts.values())
  print('frequency of least common unit is ' + str(most_frequent_units_and_counts[-1][1] / total_count))

  return (
    unit_counts_to_normalized_frequencies_for_given_units(most_frequent_units, book_to_unit_counts, normalization_method),
    most_frequent_units)

# Returns a 2d array
# where array[book index][unit index] = zscore
# and the book index matches the index of the same book in the given book_to_unit_counts
# and the unit index matches the index of the same unit in the given list of units.
#
# units: List, the units the frequencies should be calculated for
# book_to_unit_counts: List<Counter>, the number of times every unit appears in each book
def unit_counts_to_normalized_frequencies_for_given_units(units, book_to_unit_counts, normalization_method):
  # 2d List of book to unit to frequency
  # where the book indexes match those in book_to_unit_counts
  # and the unit indexes match those in units
  book_to_unit_frequencies = _find_book_to_unit_frequencies(book_to_unit_counts, units)

  book_to_normalized_unit_frequency = _normalize_frequencies(book_to_unit_frequencies, normalization_method)
  return book_to_normalized_unit_frequency

# Returns a tuple where the left side is the relative frequencies of all units
# (as a fraction of the total units in each book)
# in the form of a 2d List[book][unit]
# and the right side is the list of all units
#
# book_to_unit_counts: List<Counter>, the number of times every unit appears in each book
def unit_counts_to_all_raw_frequencies(book_to_unit_counts):
  units = set()
  for counter in book_to_unit_counts:
    units.update(counter.keys())

  unit_list = list(units)
  return _find_book_to_unit_frequencies(book_to_unit_counts, unit_list), unit_list

# Returns the relative frequencies of the given units
# (as a fraction of the total units in each book)
# in the form of a 2d List[book][unit]
#
# book_to_unit_counts: List<Counter>, the number of times every unit appears in each book
# units: List of units we're interested in
def _find_book_to_unit_frequencies(book_to_unit_counts, units):
  num_books = len(book_to_unit_counts)
  num_units = len(units)

  book_to_unit_frequencies = [None] * num_books
  for book_index, unit_counts in enumerate(book_to_unit_counts):
    total_units = sum(unit_counts.values()) # Counter.total() not added till 3.10
    book_to_unit_frequencies[book_index] = [0] * num_units
    for unit_index, unit in enumerate(units):
      book_to_unit_frequencies[book_index][unit_index] = unit_counts[unit] / total_units

  return book_to_unit_frequencies

# Normalizes the given relative frequencies using the given method.
#
# book_to_unit_frequencies: 2d List of book to unit to frequency
# normalization_method: String.  If 'zscore', then for each unit the results will have a mean of 0 and std dev of 1.
#   If 'simple', then for each unit the results will be scaled to have a minimum of -1 and a maximum of 1.
def _normalize_frequencies(book_to_unit_frequencies, normalization_method):
  if normalization_method == 'zscore':
    return _normalize_frequencies_to_zscore(book_to_unit_frequencies)
  elif normalization_method == 'simple':
    return _normalize_frequencies_simple(book_to_unit_frequencies)
  else:
    raise ValueError(normalization_method)

# Normalizes the given relative frequencies to zscores.
# For each unit the results will have a mean of 0 and std dev of 1.
#
# book_to_unit_frequencies: 2d List of book to unit to frequency
def _normalize_frequencies_to_zscore(book_to_unit_frequencies):
  # Invert the 2d List.
  # Need to convert the Zip to a List so that it can be iterated twice.
  unit_to_book_to_frequencies = list(zip(*book_to_unit_frequencies))

  means = [fmean(frequencies) for frequencies in unit_to_book_to_frequencies]
  std_devs = [stdev(frequencies) for frequencies in unit_to_book_to_frequencies]

  book_to_unit_zscores = [None] * len(book_to_unit_frequencies)
  for book_index, unit_frequencies in enumerate(book_to_unit_frequencies):
    book_to_unit_zscores[book_index] = [(freq - means[unit_index]) / std_devs[unit_index] for unit_index, freq in enumerate(unit_frequencies)]

  return book_to_unit_zscores

def _normalize_frequencies_simple(book_to_unit_frequencies):
  # Invert the 2d List.
  # Need to convert the Zip to a List so that it can be iterated twice.
  unit_to_book_to_frequencies = list(zip(*book_to_unit_frequencies))

  maxes = [max(book_to_freqs) for book_to_freqs in unit_to_book_to_frequencies]
  mins = [min(book_to_freqs) for book_to_freqs in unit_to_book_to_frequencies]
  multipliers = [2 / (max_freq - min_freq) for max_freq, min_freq in zip(maxes, mins)] # one unit per unit

  book_to_unit_normalized_frequencies = [None] * len(book_to_unit_frequencies)
  for book_index, unit_frequencies in enumerate(book_to_unit_frequencies):
    book_to_unit_normalized_frequencies[book_index] = [(x - min_freq) * multiplier - 1 for x, min_freq, multiplier in zip(unit_frequencies, mins, multipliers)]
  return book_to_unit_normalized_frequencies
