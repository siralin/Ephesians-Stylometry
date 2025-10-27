from read_text_utils import read_texts
from word_utils import calculate_raw_word_frequencies, calculate_normalized_word_frequencies
from scatter_plot_utils import generate_scatter_plot
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA

book_to_text = read_texts()

# Find 99 'most common' words (p.264 Hutchinson)
NUM_WORDS_WANTED = 99

# words: a List of the most frequent words
#
# book_to_normalized_word_frequency: a 2d List[book index][word index]
# where the book index matches the index of the same book in book_to_word_counts and book_to_text
# and the word index matches the index of the same word in words.
book_to_normalized_word_frequency, words = calculate_normalized_word_frequencies(
  book_to_text, NUM_WORDS_WANTED, 'zscore')

data = pd.DataFrame(book_to_normalized_word_frequency)
pca = PCA(n_components=2, svd_solver='full').fit(data)
print(pca.components_)
print(pca.explained_variance_)

# There are two 'components' arrays, each with one element per word
# We can graph them to see how important each word is to the PCA.

fig = plt.figure(1, figsize=(8, 6))
ax = fig.add_subplot()

scatter = ax.scatter(
  pca.components_[0],
  pca.components_[1],
)

for i, word in enumerate(words):
  ax.annotate(word, (pca.components_[0][i], pca.components_[1][i]))

fig.tight_layout()
plt.show()

# each is a 99-dimensional vector
#x_vector, y_vector = pca.components_

#print(x_vector, y_vector)
#print(pca.singular_values_)

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