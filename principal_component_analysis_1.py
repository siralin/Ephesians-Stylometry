from read_text_utils import read_texts
from word_utils import calculate_raw_word_frequencies, calculate_normalized_word_frequencies
from scatter_plot_utils import generate_scatter_plot, generate_component_plot
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA

"""
Generates Figures 1a and 1b for the thesis.
1a is the influence of the top 99 words on the two principal component vectors.
1b is the results of arranging all books (including Septuagint) according to those vectors.
"""

book_to_text = read_texts()

# Find 99 most common words (p.264 Hutchinson)
NUM_WORDS_WANTED = 99
NORMALIZATION_METHOD = 'zscore'

# words: a List of the most frequent words
#
# book_to_normalized_word_frequency: a 2d List[book index][word index]
# where the book index matches the index of the same book in book_to_word_counts and book_to_text
# and the word index matches the index of the same word in words.
book_to_normalized_word_frequency, words = calculate_normalized_word_frequencies(
  book_to_text, NUM_WORDS_WANTED, NORMALIZATION_METHOD)

print(words)

generate_component_plot(book_to_normalized_word_frequency, words, title="Figure 1a")
plt.show()

generate_scatter_plot(book_to_normalized_word_frequency, book_to_text.keys(), title="Figure 1b")
plt.show()
