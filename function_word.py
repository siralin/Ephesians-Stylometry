from function_word_utils import calculate_normalized_function_word_frequencies, FUNCTION_WORDS
from read_nt_text_utils import read_normalized_texts
from scatter_plot_utils import generate_scatter_plot
from dendrogram_utils import generate_dendrogram, check_dendrogram_valid
import matplotlib.pyplot as plt

# TODO feel free to change all these parameters
NUM_FUNCTION_WORDS_WANTED = 10
NORMALIZATION_METHOD = 'simple' # 'zscore' or 'simple'
LINKAGE_ALGORITHM = 'ward'
DISTANCE_METRIC = 'euclidean'

book_to_text = read_normalized_texts()
function_words = FUNCTION_WORDS[:NUM_FUNCTION_WORDS_WANTED]

# book_to_normalized_word_frequency: a 2d List[book index][word index]
# where the book index matches the index of the same book in book_to_word_counts and book_to_text
# and the word index matches the index of the same word in function_words.
book_to_normalized_word_frequency = calculate_normalized_function_word_frequencies(
  book_to_text, function_words, NORMALIZATION_METHOD)

# In Python 3.7+, dictionary iteration order is always the same,
# so the keys() call will produce book titles in the right order.
generate_scatter_plot(book_to_normalized_word_frequency, book_to_text.keys())
title = str(NUM_FUNCTION_WORDS_WANTED) + " most frequent function words (" + NORMALIZATION_METHOD + ")"
plt.gca().update({"title":title})
plt.show()

generate_dendrogram(book_to_normalized_word_frequency, book_to_text.keys(), LINKAGE_ALGORITHM, DISTANCE_METRIC)
print(check_dendrogram_valid())
plt.show()
