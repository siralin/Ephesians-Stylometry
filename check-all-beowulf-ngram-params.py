import matplotlib.pyplot as plt
import beowulf_utils
import delta_plot_utils

# we now have the text of each book, in order without spaces
# but we'll put spaces between books to keep them separate
books = beowulf_utils.read_book_texts()
del books['3-john'] # too short
del books['2-john'] # too short
del books['philemon'] # too short

all_text = ""
for book, book_text in books.items():
  all_text += book_text + " "

for ngram_size in [2, 3, 4]:
  for num_bigrams_wanted in range(2, 100):
    interesting_bigrams = beowulf_utils.find_interesting_bigrams(all_text, num_bigrams_wanted, ngram_size)
    bigram_to_book_to_frequency = beowulf_utils.calculate_ngram_frequencies(interesting_bigrams, books)
    bigram_to_book_to_norm_freq = beowulf_utils.normalize_ngram_frequencies(bigram_to_book_to_frequency)

    new_matrix = [list(row) for row in zip(*bigram_to_book_to_norm_freq)]

    for linkage_algorithm in ['complete', 'average', 'weighted', 'centroid', 'median', 'ward']:
      for distance_metric in ['canberra', 'chebyshev', 'cityblock', 'euclidean', 'hamming', 'jaccard', 'matching', 'minkowski', 'rogerstanimoto', 'russellrao', 'seuclidean', 'sokalmichener', 'sokalsneath', 'sqeuclidean', 'yule']:
        # removed 'dice' because it produces negative distances
        # removed jensenshannon, kulczynski1, 'correlation',  because it produces non-finite distances
        # 'mahalanobis' needed more books
        # braycurtis is about species
        # 'single', is ugly

        if linkage_algorithm in ['centroid', 'median', 'ward'] and distance_metric != 'euclidean':
          continue

        desc = " ".join([str(ngram_size), str(num_bigrams_wanted), linkage_algorithm, distance_metric])
        print('testing ' + desc)

        delta_plot_utils.generate_dendrogram(new_matrix, list(books), linkage_algorithm, distance_metric)
        if delta_plot_utils.check_dendrogram_valid(6): # ONLY BECAUSE PHILEMON EXCLUDED
          filename = '-'.join(['dendrogram', str(ngram_size) + 'gram', str(num_bigrams_wanted), linkage_algorithm, distance_metric])
          plt.savefig(filename + '.png', format='png', dpi=100)
          #plt.show()
        plt.close() # otherwise they stay open and consume all the memory

# differences from my 2-gram method:
#   different number of 2-grams analyzed
#   beowulf by default keeps spaces but doesn't include them in bigrams
#   normalized differently (zscores vs simple stretching)
#   distances calculated differently (PCA vs calculation with euclidean etc)
