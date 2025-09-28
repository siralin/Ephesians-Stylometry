from sentence_length_utils import read_sentence_lengths
import re
import sys
import matplotlib.pyplot as plt
from general_utils import UNCONTESTED_PAUL_BOOKS, CONTESTED_PAUL_BOOKS

# Read in all the (non-normalized) NT texts,
# so that we have a dictionary of book name to complete text.
# Record the length of each sentence.
# Graph the sentence lengths:
#   x-axis: number of words (bucketed)
#   y-axis: frequency (as a fraction of total sentences in the book)
#   one line per book
book_to_sentence_lengths = read_sentence_lengths()

# Find max sentence length.
# Decide on buckets for sentence lengths (1-5 words, 6-10, etc).
max_lengths = [max(x) for x in book_to_sentence_lengths.values()]
max_length = max(max_lengths)
if max_length != 166:
  raise ValueError("error: max length is " + str(max_length))

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
