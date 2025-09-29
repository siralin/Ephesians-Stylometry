from sentence_length_utils import read_sentence_lengths
from general_utils import UNCONTESTED_PAUL_BOOKS, CONTESTED_PAUL_BOOKS, BOOK_NAMES
from statistics import fmean

book_to_lengths = read_sentence_lengths()
pauline_book_to_lengths = {b: book_to_lengths[b] for b in UNCONTESTED_PAUL_BOOKS}
#nonpauline_book_to_lengths = {
#  b: book_to_lengths[b] for b in BOOK_NAMES if b not in UNCONTESTED_PAUL_BOOKS and b not in CONTESTED_PAUL_BOOKS}

shortest_length = min([min(x) for x in book_to_lengths.values()])
longest_length = max([max(x) for x in book_to_lengths.values()])

#print(shortest_length, longest_length, len(book_to_lengths), len(pauline_book_to_lengths), len(nonpauline_book_to_lengths))

def count_matches(x_to_lengths, length):
  return sum([lengths.count(length) for lengths in x_to_lengths.values()])

average_pauline_matches = 1 + fmean([count_matches(pauline_book_to_lengths, l) for l in range(shortest_length, longest_length)])
print(average_pauline_matches)

# Assume non-Pauline sentences have an equal likelihood of being any length from 2 to 166 words?
pauline_probability = 1
nonpauline_probability = 1
for length in book_to_lengths['ephesians']:
  pauline_matches = count_matches(pauline_book_to_lengths, length) + 1
  total_matches = pauline_matches + average_pauline_matches
  print('\tlength:' + str(length) + ' ' + str(pauline_matches) + ' ' + str(total_matches))

  pauline_probability *= pauline_matches / total_matches
  nonpauline_probability *= 1 - pauline_matches / total_matches
  print('\t\t' + str(pauline_probability) + ' ' + str(nonpauline_probability))

print(pauline_probability, nonpauline_probability)
print(pauline_probability / (pauline_probability + nonpauline_probability))

"""
num_pauline_sentences = sum([len(lengths) for lengths in pauline_book_to_lengths.values()])
num_nonpauline_sentences = sum([len(lengths) for lengths in nonpauline_book_to_lengths.values()])
print(num_pauline_sentences, num_nonpauline_sentences)

def count_lengths(x_to_lengths):
  return sum([lengths.count(length) for lengths in x_to_lengths.values()])

#pauline_probability = 0
#nonpauline_probability = 0
pauline_probability = 1
nonpauline_probability = 1
for length in book_to_lengths['mark']:
  #total_matches = count_lengths(book_to_lengths) + 2

  pauline_matches = count_lengths(pauline_book_to_lengths)
  nonpauline_matches = count_lengths(nonpauline_book_to_lengths)
  if pauline_matches == 0 and nonpauline_matches == 0:
    nonpauline_matches += 4
    #continue # probably would make more sense as a continuous distribution?

  # Add 1 to each following the Rule of succession to avoid 0 probabilities
  #pauline_matches = count_lengths(pauline_book_to_lengths) + 1
  #nonpauline_matches = count_lengths(nonpauline_book_to_lengths) + 1
  total_matches = pauline_matches + nonpauline_matches
  print('\tlength:' + str(length) + ' ' + str(pauline_matches) + ' ' + str(nonpauline_matches))

  #if pauline_matches == 0 or nonpauline_matches == 0: # This is weird and definitely wrong
  #  continue

  #pauline_probability += pauline_matches
  #nonpauline_probability += nonpauline_matches
  pauline_probability *= max(1, pauline_matches) / total_matches * num_nonpauline_sentences / 1100
  nonpauline_probability *= max(4, nonpauline_matches) / total_matches * num_pauline_sentences / 1100
  print('\t\t' + str(pauline_probability) + ' ' + str(nonpauline_probability))

print(pauline_probability, nonpauline_probability)
print(pauline_probability / (pauline_probability + nonpauline_probability))
"""