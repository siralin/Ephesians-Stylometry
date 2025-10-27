from read_text_utils import read_texts
from word_utils import calculate_raw_word_frequencies, calculate_normalized_word_frequencies
from scatter_plot_utils import generate_scatter_plot, generate_component_plot
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA

book_to_text = read_texts()

# Find 99 'most common' words (p.264 Hutchinson)
NUM_WORDS_WANTED = 99
NORMALIZATION_METHOD = 'zscore'

# words: a List of the most frequent words
#
# book_to_normalized_word_frequency: a 2d List[book index][word index]
# where the book index matches the index of the same book in book_to_word_counts and book_to_text
# and the word index matches the index of the same word in words.
book_to_normalized_word_frequency, words = calculate_normalized_word_frequencies(
  book_to_text, NUM_WORDS_WANTED, NORMALIZATION_METHOD)

generate_component_plot(book_to_normalized_word_frequency, words)
plt.show()

title = str(NUM_WORDS_WANTED) + " most frequent words (" + NORMALIZATION_METHOD + ")"
generate_scatter_plot(book_to_normalized_word_frequency, book_to_text.keys(), title=title)
plt.show()

"""
# words: a List of all words
#
# book_to_raw_word_frequency: a 2d List[book index][word index]
# where the book index matches the index of the same book in book_to_word_counts and book_to_text
# and the word index matches the index of the same word in words.
book_to_raw_word_frequency, words = calculate_raw_word_frequencies(book_to_text)

# Find 99 'most common' words (p.264 Hutchinson)
# These are determined to be the 'most common' by adding up their relative frequencies. ('Lyrical Drama' p. 64)
NUM_WORDS_WANTED = 99

word_and_total_frequency = []
for word_index, word in enumerate(words):
  total_frequency = sum([fs[word_index] for fs in book_to_raw_word_frequency])
  word_and_total_frequency.append((word, total_frequency))
word_and_total_frequency.sort(key=lambda tup: tup[1], reverse=True)
print(word_and_total_frequency[:10])

most_common_words = [watf[0] for watf in word_and_total_frequency[:99]]
print(most_common_words)
"""