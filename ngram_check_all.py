from ngram_utils import calculate_normalized_ngram_frequencies
from read_text_utils import read_normalized_texts
from ngram_scatter_plot_utils import generate_scatter_plot
from ngram_dendrogram_utils import generate_dendrogram, check_dendrogram_valid, save_dendrogram
import matplotlib.pyplot as plt
from collections import Counter

book_to_text = read_normalized_texts()

for merge_words in [False, True]: # True has to be second because it modifies the dict
  if merge_words:
    for book, text in book_to_text.items():
      book_to_text.update({book: "".join(text.split())})

  for ngram_size in range(1, 5):
    for num_ngrams_wanted in range(1, 100):
      for normalization_method in ['simple', 'zscore']:
        book_to_normalized_ngram_frequency, ngrams = calculate_normalized_ngram_frequencies(
          book_to_text, num_ngrams_wanted, ngram_size, normalization_method)

        for linkage_algorithm in ['complete', 'average', 'weighted', 'centroid', 'median', 'ward']:
          for distance_metric in ['canberra', 'chebyshev', 'cityblock', 'euclidean', 'hamming', 'jaccard', 'matching', 'minkowski', 'rogerstanimoto', 'russellrao', 'seuclidean', 'sokalmichener', 'sokalsneath', 'sqeuclidean', 'yule']:
            if linkage_algorithm in ['centroid', 'median', 'ward'] and distance_metric != 'euclidean':
              continue

            desc = ' '.join([str(num_ngrams_wanted), str(ngram_size), str(merge_words), normalization_method, linkage_algorithm, distance_metric])
            print('testing ' + desc)
            generate_dendrogram(book_to_normalized_ngram_frequency, book_to_text.keys())
            if (check_dendrogram_valid()):
              #plt.show()
              save_dendrogram([merge_words, ngram_size, 'gram', num_ngrams_wanted, normalization_method, linkage_algorithm, distance_metric])
            plt.close() # otherwise they stay open and consume all the memory
