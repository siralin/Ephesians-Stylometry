from part_utils import calculate_normalized_part_frequencies
from read_text_utils import read_parts_of_speech
from scatter_plot_utils import generate_scatter_plot
from dendrogram_utils import generate_dendrogram, check_dendrogram_valid
import matplotlib.pyplot as plt

# TODO feel free to change all these parameters
NUM_PARTS_WANTED = 40
NORMALIZATION_METHOD = 'simple' # 'zscore' or 'simple'
LINKAGE_ALGORITHM = 'ward'
DISTANCE_METRIC = 'euclidean'

book_to_text = read_parts_of_speech()

# parts: a List of the most frequent parts of speech
#
# book_to_normalized_part_frequency: a 2d List[book index][part index]
# where the book index matches the index of the same book in book_to_part_counts and book_to_text
# and the part index matches the index of the same part in parts.
book_to_normalized_part_frequency, parts = calculate_normalized_part_frequencies(
  book_to_text, NUM_PARTS_WANTED, NORMALIZATION_METHOD)

# In Python 3.7+, dictionary iteration order is always the same,
# so the keys() call will produce book titles in the right order.
generate_scatter_plot(book_to_normalized_part_frequency, book_to_text.keys())
title = str(NUM_PARTS_WANTED) + " most frequent parts (" + NORMALIZATION_METHOD + ")"
plt.gca().update({"title":title})
plt.show()

generate_dendrogram(book_to_normalized_part_frequency, book_to_text.keys(), LINKAGE_ALGORITHM, DISTANCE_METRIC)
print(check_dendrogram_valid())
plt.show()
