import matplotlib.pyplot as plt
from scipy.cluster.hierarchy import dendrogram, linkage
import beowulf_utils

NGRAM_SIZE = beowulf_utils.NGRAM_SIZE
NUM_NGRAMS = beowulf_utils.NUM_NGRAMS

# we now have the text of each book, in order without spaces
# but we'll put spaces between books to keep them separate
books = beowulf_utils.read_book_texts()

all_text = ""
for book, book_text in books.items():
  all_text += book_text + " "

interesting_bigrams = beowulf_utils.find_interesting_bigrams(all_text)
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
#plt.savefig('dendrogram_trigram.eps', format='eps', dpi=1000)
plt.show()

# differences from my 2-gram method:
#   different number of 2-grams analyzed
#   this one keeps spaces but doesn't include them in bigrams
#   normalized differently (zscores vs simple stretching)
