from word_utils import calculate_normalized_word_frequencies
from read_nt_text_utils import read_normalized_texts
from dendrogram_utils import generate_dendrogram, check_dendrogram_valid, save_dendrogram
import matplotlib.pyplot as plt

book_to_text = read_normalized_texts()

# Delete the shortest book(s) as they incline to outliers.
del book_to_text['3 john']
del book_to_text['2 john']
del book_to_text['philemon']

for num_words_wanted in range(1, 100):
  for normalization_method in ['simple', 'zscore']:
    book_to_normalized_word_frequency, words = calculate_normalized_word_frequencies(
      book_to_text, num_words_wanted, normalization_method)

    for linkage_algorithm in ['complete', 'average', 'weighted', 'centroid', 'median', 'ward']:
      for distance_metric in ['canberra', 'chebyshev', 'cityblock', 'euclidean', 'hamming', 'jaccard', 'matching', 'minkowski', 'rogerstanimoto', 'russellrao', 'seuclidean', 'sokalmichener', 'sokalsneath', 'sqeuclidean', 'yule']:
        if linkage_algorithm in ['centroid', 'median', 'ward'] and distance_metric != 'euclidean':
          continue

        desc = [str(num_words_wanted), normalization_method, linkage_algorithm, distance_metric]
        print('testing ' + ' '.join(desc))
        generate_dendrogram(book_to_normalized_word_frequency, book_to_text.keys(), linkage_algorithm, distance_metric)
        if (check_dendrogram_valid(book_to_text.keys())):
          #plt.show()
          save_dendrogram(desc)
        plt.close() # otherwise they stay open and consume all the memory
