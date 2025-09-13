import matplotlib.pyplot as plt
from scipy.cluster.hierarchy import dendrogram, linkage
import beowulf_utils

# we now have the text of each book, in order without spaces
# but we'll put spaces between books to keep them separate
books = beowulf_utils.read_book_texts()

all_text = ""
for book, book_text in books.items():
  all_text += book_text + " "

ngram_size = 2
num_bigrams_wanted = 10

interesting_bigrams = beowulf_utils.find_interesting_bigrams(all_text, num_bigrams_wanted, ngram_size)
bigram_to_book_to_frequency = beowulf_utils.calculate_ngram_frequencies(interesting_bigrams, books)
bigram_to_book_to_norm_freq = beowulf_utils.normalize_ngram_frequencies(bigram_to_book_to_frequency)

# TODO not sure if 2d array is oriented correctly here
new_matrix = [list(row) for row in zip(*bigram_to_book_to_norm_freq)]
Z = linkage(new_matrix, method='ward',metric='euclidean')

plt.figure(figsize=(25, 10))
plt.title('Hierarchical Clustering Dendrogram (Bigrams)')
plt.xlabel('text number')
plt.ylabel('distance')
dendrogram(
           Z,
           leaf_rotation=90.,  # rotates the x axis labels
           leaf_font_size=8.,  # font size for the x axis labels
           labels=list(books))

ax = plt.gca()
x_labels = ax.get_xmajorticklabels()
for x in x_labels:
  x.set_color(beowulf_utils.get_label_color(x.get_text()))

plt.savefig('dendrogram_' + str(ngram_size) + 'gram-' + str(num_bigrams_wanted) + '.png', format='png', dpi=100)
plt.show()

# differences from my 2-gram method:
#   different number of 2-grams analyzed
#   beowulf by default keeps spaces but doesn't include them in bigrams
#   normalized differently (zscores vs simple stretching)
