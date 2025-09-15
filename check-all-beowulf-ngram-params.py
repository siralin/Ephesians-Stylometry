import matplotlib.pyplot as plt
import beowulf_utils
import delta_plot_utils

# we now have the text of each book, in order without spaces
# but we'll put spaces between books to keep them separate
books = beowulf_utils.read_book_texts()

all_text = ""
for book, book_text in books.items():
  all_text += book_text + " "

# these are best with ward, euclidean
ngram_size = 2
num_bigrams_wanted = 10
linkage_algorithm = 'ward'
distance_metric = 'euclidean'

# https://aclanthology.org/W15-0709.pdf claims cosine is best (for french, german, english)
#ngram_size = 2
#num_bigrams_wanted = 30
#linkage_algorithm = 'average'
#distance_metric = 'cosine'

interesting_bigrams = beowulf_utils.find_interesting_bigrams(all_text, num_bigrams_wanted, ngram_size)
bigram_to_book_to_frequency = beowulf_utils.calculate_ngram_frequencies(interesting_bigrams, books)
bigram_to_book_to_norm_freq = beowulf_utils.normalize_ngram_frequencies(bigram_to_book_to_frequency)

new_matrix = [list(row) for row in zip(*bigram_to_book_to_norm_freq)]
delta_plot_utils.generate_dendrogram(new_matrix, list(books), linkage_algorithm, distance_metric)
delta_plot_utils.check_dendrogram_valid()
# differences from my 2-gram method:
#   different number of 2-grams analyzed
#   beowulf by default keeps spaces but doesn't include them in bigrams
#   normalized differently (zscores vs simple stretching)
#   distances calculated differently (PCA vs calculation with euclidean etc)
