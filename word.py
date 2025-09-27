from word_utils import calculate_normalized_word_frequencies
from read_text_utils import read_normalized_texts
from scatter_plot_utils import generate_scatter_plot
from dendrogram_utils import generate_dendrogram, check_dendrogram_valid
import matplotlib.pyplot as plt

# TODO feel free to change all these parameters
NUM_WORDS_WANTED = 40
NORMALIZATION_METHOD = 'simple' # 'zscore' or 'simple'
LINKAGE_ALGORITHM = 'ward'
DISTANCE_METRIC = 'euclidean'

book_to_text = read_normalized_texts()

# words: a List of the most frequent words
#
# book_to_normalized_word_frequency: a 2d List[book index][word index]
# where the book index matches the index of the same book in book_to_word_counts and book_to_text
# and the word index matches the index of the same word in words.
book_to_normalized_word_frequency, words = calculate_normalized_word_frequencies(
  book_to_text, NUM_WORDS_WANTED, NORMALIZATION_METHOD)

# In Python 3.7+, dictionary iteration order is always the same,
# so the keys() call will produce book titles in the right order.
generate_scatter_plot(book_to_normalized_word_frequency, book_to_text.keys())
title = str(NUM_WORDS_WANTED) + " most frequent words (" + NORMALIZATION_METHOD + ")"
plt.gca().update({"title":title})
plt.show()

generate_dendrogram(book_to_normalized_word_frequency, book_to_text.keys(), LINKAGE_ALGORITHM, DISTANCE_METRIC)
print(check_dendrogram_valid())
plt.show()
