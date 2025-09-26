from ngram_utils import ngram_counts_to_normalized_frequencies
from text_normalization_utils import read_normalized_texts
from ngram_scatter_plot_utils import generate_scatter_plot
from ngram_dendrogram_utils import generate_dendrogram, check_dendrogram_valid
import matplotlib.pyplot as plt
from collections import Counter

# TODO determine best values here
NGRAM_SIZE = 2
NUM_NGRAMS_WANTED = 40 # maximum reasonable value is 25 ^ NGRAM_SIZE
MERGE_WORDS = False # Whether to remove the spaces in the normalized text.
NORMALIZATION_METHOD = 'zscore' # 'zscore' or 'simple'

book_to_text = read_normalized_texts()
if MERGE_WORDS:
  # TODO remove spaces
  pass

# first, calculate frequency of every possible ngram in each book.
# This is a list of Counters, one for each ngram
book_to_ngram_counts = [None] * len(book_to_text)
overall_ngram_counts = Counter()

for index, book in enumerate(book_to_text):
  text = book_to_text[book]
  book_to_ngram_counts[index] = Counter()
  for i in range(0, len(text) - 1):
    ngram = text[i:i + NGRAM_SIZE]

    # can remove ngrams containing spaces if you want
    if " " not in ngram:
      book_to_ngram_counts[index][ngram] += 1
      overall_ngram_counts[ngram] += 1

# ngrams: a List of the most frequent ngrams
#
# book_to_normalized_ngram_frequency: a 2d List[book index][ngram index]
# where the book index matches the index of the same book in book_to_ngram_counts and book_to_text
# and the ngram index matches the index of the same ngram in ngrams.
book_to_normalized_ngram_frequency, ngrams = ngram_counts_to_normalized_frequencies(
  NUM_NGRAMS_WANTED, book_to_ngram_counts, overall_ngram_counts, NORMALIZATION_METHOD)

"""
# In Python 3.7+, dictionary iteration order is always the same,
# so the keys() call will produce book titles in the right order.
generate_scatter_plot(book_to_normalized_ngram_frequency, book_to_text.keys())
title = str(NUM_NGRAMS_WANTED) + " most frequent " + str(NGRAM_SIZE) + "grams (" + str(MERGE_WORDS) + " " + NORMALIZATION_METHOD + ")"
plt.gca().update({"title":title})
plt.show()
"""

generate_dendrogram(book_to_normalized_ngram_frequency, book_to_text.keys())
print(check_dendrogram_valid())
plt.show()

"""
# note program doesn't continue till you exit shown graph
display_graph(zscores, 0.3, -0.2)

actual_num_bigrams = len(zscores['mark']) # arbitrarily selected; they're all the same

book_to_bigram_to_frequency = [[0 for x in range(actual_num_bigrams)] for y in range(len(books))]
for book_index, book in enumerate(books):
  for bigram_index, bigram in enumerate(zscores['mark']):
    book_to_bigram_to_frequency[book_index][bigram_index] = zscores[book][bigram]

linkage_algorithm = 'ward'
distance_metric = 'euclidean'
display_dendrogram(book_to_bigram_to_frequency, list(books), linkage_algorithm, distance_metric)
"""
