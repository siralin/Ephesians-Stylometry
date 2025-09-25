from delta_utils import read_and_calculate_text_to_zscores
from delta_plot_utils import generate_dendrogram, check_dendrogram_valid, display_graph
from pprint import pprint
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.decomposition import PCA

for num_functors in range(2, 100):
  book_to_word_zscores = read_and_calculate_text_to_zscores(num_functors)
  display_graph(book_to_word_zscores, 0, 0, title="i=" + str(num_functors))
  plt.close()

  zscore_matrix = [None] * len(book_to_word_zscores)
  for i, book in enumerate(book_to_word_zscores):
    print(len(book_to_word_zscores), len(zscore_matrix), i)
    zscore_matrix[i] = [0] * num_functors
    for j, word in enumerate(book_to_word_zscores['mark']): #arbitrary choice
      zscore_matrix[i][j] = book_to_word_zscores[book][word]

  for linkage_algorithm in ['complete', 'average', 'weighted', 'centroid', 'median', 'ward']:
    for distance_metric in ['canberra', 'chebyshev', 'cityblock', 'euclidean', 'hamming', 'jaccard', 'matching', 'minkowski', 'rogerstanimoto', 'russellrao', 'seuclidean', 'sokalmichener', 'sokalsneath', 'sqeuclidean', 'yule']:

      if linkage_algorithm in ['centroid', 'median', 'ward'] and distance_metric != 'euclidean':
        continue

      desc = "-".join(["functor", str(num_functors), linkage_algorithm, distance_metric])
      print('testing ' + desc)

      generate_dendrogram(zscore_matrix, list(book_to_word_zscores.keys()), linkage_algorithm, distance_metric, 'Functors')
      if check_dendrogram_valid(): # if 6, ONLY BECAUSE PHILEMON EXCLUDED
        filename = 'dendrogram-' + desc
        plt.savefig(filename + '.png', format='png', dpi=100)
        plt.show()
      plt.close() # otherwise they stay open and consume all the memory