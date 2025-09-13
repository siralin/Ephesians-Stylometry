from delta_utils import read_normalized_texts
import matplotlib.pyplot as plt
from collections import Counter
from nltk.util import ngrams
from scipy.cluster.hierarchy import dendrogram, linkage

NGRAM_SIZE = 2
NUM_NGRAMS = 30

# calculate frequency of every possible 2-gram in each book

book_to_chapter_to_text = read_normalized_texts()

# then get rid of parallel/unique texts
del book_to_chapter_to_text['ephesiansparallel']
del book_to_chapter_to_text['colossiansparallel']
del book_to_chapter_to_text['ephesiansunique']
del book_to_chapter_to_text['colossiansunique']

# (Note that if you don't delete either the originals or the parallel/unique texts,
# you get incorrect information about the most common words/bigrams/etc)

books = {}
for book, chapter_to_text in book_to_chapter_to_text.items():
  book_text = ''
  for c in range(0, len(chapter_to_text)):
    book_text += chapter_to_text[c+1]
  books[book] = book_text #''.join(book_text.split())

# we now have the text of each book, in order with spaces

all_text = ""
for book, book_text in books.items():
  all_text += book_text + " "

# Take the NUM_NGRAMS most common bigrams that don't include spaces.
all_bigrams = ngrams(all_text, NGRAM_SIZE) # includes spaces
letter_bigrams = [bi for bi in all_bigrams if " " not in bi]
bigram_counts = Counter(letter_bigrams)
interesting_bigrams = bigram_counts.most_common(NUM_NGRAMS)

# Convert counts to frequencies.
#   (Within each book, the number of ngram occurrences
#    divided by the number of non-space characters.)

num_books = len(books)
print("num books", num_books)
bigram_to_book_to_frequency = [[0 for x in range(num_books)] for y in range(NUM_NGRAMS)]

for book_index, book in enumerate(books):
  book_text = books[book]
  text_length = len(book_text) - book_text.count(' ')
  for bigram_index, bigram in enumerate(interesting_bigrams):
    bigram_count = book_text.count("".join(bigram[0]))
    bigram_to_book_to_frequency[bigram_index][book_index] = bigram_count / text_length
  print("book " + str(book_index) + " is " + book)

# Normalize frequencies _per ngram_ (cross-book) to between -1, 1
bigram_to_book_to_norm_freq = [[]] * NUM_NGRAMS
for bigram_index in range(NUM_NGRAMS):
  max_freq = max(bigram_to_book_to_frequency[bigram_index])
  min_freq = min(bigram_to_book_to_frequency[bigram_index])
  multiplier = 2 / (max_freq - min_freq)
  bigram_to_book_to_norm_freq[bigram_index] = [(x - min_freq) * multiplier - 1 for x in bigram_to_book_to_frequency[bigram_index]]

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
#   normalized differently (zscores vs simple stretching)

"""
book_to_ngram_counts = {}
total_ngram_counts = Counter()

for book, text in books.items():
  book_to_ngram_counts[book] = Counter()
  for i in range(0, len(text) - 1):
    ngram = text[i:i + NGRAM_SIZE]

    book_to_ngram_counts[book][ngram] += 1
    total_ngram_counts[ngram] += 1

zscores = word_counts_to_zscores(round(math.pow(24, NGRAM_SIZE)), book_to_ngram_counts, total_ngram_counts)

display_graph(zscores, 0.4, -0.2)
"""