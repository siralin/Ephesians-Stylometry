from ngram_utils import calculate_normalized_ngram_frequencies
from read_text_utils import read_normalized_texts
from scatter_plot_utils import generate_scatter_plot
from dendrogram_utils import generate_dendrogram, check_dendrogram_valid
import matplotlib.pyplot as plt

# TODO feel free to change all these parameters
NGRAM_SIZE = 2
NUM_NGRAMS_WANTED = 40 # maximum reasonable value is 25 ^ NGRAM_SIZE
MERGE_WORDS = True # Whether to remove the spaces in the normalized text.
NORMALIZATION_METHOD = 'zscore' # 'zscore' or 'simple'
LINKAGE_ALGORITHM = 'complete'
DISTANCE_METRIC = 'cosine'

book_to_text = read_normalized_texts()
if MERGE_WORDS:
  for book, text in book_to_text.items():
    book_to_text.update({book: "".join(text.split())})

# ngrams: a List of the most frequent ngrams
#
# book_to_normalized_ngram_frequency: a 2d List[book index][ngram index]
# where the book index matches the index of the same book in book_to_ngram_counts and book_to_text
# and the ngram index matches the index of the same ngram in ngrams.
book_to_normalized_ngram_frequency, ngrams = calculate_normalized_ngram_frequencies(
  book_to_text, NUM_NGRAMS_WANTED, NGRAM_SIZE, NORMALIZATION_METHOD)

# In Python 3.7+, dictionary iteration order is always the same,
# so the keys() call will produce book titles in the right order.
generate_scatter_plot(book_to_normalized_ngram_frequency, book_to_text.keys())
title = str(NUM_NGRAMS_WANTED) + " most frequent " + str(NGRAM_SIZE) + "grams (" + str(MERGE_WORDS) + " " + NORMALIZATION_METHOD + ")"
plt.gca().update({"title":title})
plt.show()

generate_dendrogram(book_to_normalized_ngram_frequency, book_to_text.keys(), LINKAGE_ALGORITHM, DISTANCE_METRIC)
plt.show()
