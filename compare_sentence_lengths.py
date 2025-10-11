import matplotlib.pyplot as plt
from sentence_length_utils import read_sentence_lengths
from general_utils import BOOK_NAMES, UNCONTESTED_PAUL_BOOKS, CONTESTED_PAUL_BOOKS
import sys
import functools as f
from operator import add

unsorted_book_to_sentence_lengths = read_sentence_lengths()
book_to_sentence_lengths = dict([(b, unsorted_book_to_sentence_lengths[b]) for b in UNCONTESTED_PAUL_BOOKS])
book_to_sentence_lengths['All Pauline'] = f.reduce(add, book_to_sentence_lengths.values())
book_to_sentence_lengths['Ephesians'] = unsorted_book_to_sentence_lengths['Ephesians']

# Find max sentence length.
# Decide on buckets for sentence lengths (1-5 words, 6-10, etc).
max_lengths = [max(x) for x in book_to_sentence_lengths.values()]
max_length = max(max_lengths)
#if max_length != 166:
#  print("error: max length is " + str(max_length))
#  sys.exit()

# Let's go with buckets with a range of 10.

fig = plt.figure()
ax = fig.add_axes([0.1, 0.1, 0.7, 0.8])

for book, sentence_lengths in book_to_sentence_lengths.items():
  num_sentences = len(sentence_lengths)

  # desired format: list of number of sentences (divided by total sentences) in each bucket
  buckets = [0] * 19
  for sentence_length in sentence_lengths:
    buckets[(sentence_length - 1) // 10] += 1
  frequency_buckets = [b / num_sentences for b in buckets]

  linestyle = 'dotted'
  if book in UNCONTESTED_PAUL_BOOKS:
    linestyle = 'solid'
  elif book in CONTESTED_PAUL_BOOKS:
    linestyle = 'dashed'

  ax.plot(range(1, 20), frequency_buckets, label=book, linestyle=linestyle)
  ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0.)

plt.show()