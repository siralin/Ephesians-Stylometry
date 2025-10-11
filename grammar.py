from grammar_utils import calculate_normalized_part_of_speech_ngram_frequencies
from read_text_utils import read_parts_of_speech
from scatter_plot_utils import generate_scatter_plot
from dendrogram_utils import generate_dendrogram, check_dendrogram_valid
import matplotlib.pyplot as plt

# In this script, an ngram is a sequence of parts of speech

# TODO feel free to change all these parameters
NGRAM_SIZE = 3
NUM_NGRAMS_WANTED = 30
NORMALIZATION_METHOD = 'simple' # 'zscore' or 'simple'
LINKAGE_ALGORITHM = 'complete'
DISTANCE_METRIC = 'euclidean'

book_to_text = read_parts_of_speech()

# ngrams: a List of the most frequent ngrams
#
# book_to_normalized_ngram_frequency: a 2d List[book index][ngram index]
#   where the book index matches the index of the same book in book_to_text
#   and the ngram index matches the index of the same ngram in ngrams.
book_to_normalized_ngram_frequency, ngrams = calculate_normalized_part_of_speech_ngram_frequencies(
  book_to_text, NUM_NGRAMS_WANTED, NGRAM_SIZE, NORMALIZATION_METHOD)

# In Python 3.7+, dictionary iteration order is always the same,
# so the keys() call will produce book titles in the right order.
generate_scatter_plot(book_to_normalized_ngram_frequency, book_to_text.keys())
title = str(NUM_NGRAMS_WANTED) + " most frequent " + str(NGRAM_SIZE) + "part-grams (" + NORMALIZATION_METHOD + ")"
plt.gca().update({"title":title})
plt.show()

generate_dendrogram(book_to_normalized_ngram_frequency, book_to_text.keys(), LINKAGE_ALGORITHM, DISTANCE_METRIC)
print(check_dendrogram_valid())
plt.show()
