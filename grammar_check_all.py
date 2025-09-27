from grammar_utils import calculate_normalized_part_of_speech_ngram_frequencies
from read_text_utils import read_parts_of_speech
from dendrogram_utils import generate_dendrogram, check_dendrogram_valid, save_dendrogram
import matplotlib.pyplot as plt

book_to_text = read_parts_of_speech()

for ngram_size in range(1, 5):
  for num_ngrams_wanted in range(1, 100):
    for normalization_method in ['simple', 'zscore']:
      book_to_normalized_ngram_frequency, ngrams = calculate_normalized_part_of_speech_ngram_frequencies(
        book_to_text, num_ngrams_wanted, ngram_size, normalization_method)

      for linkage_algorithm in ['complete', 'average', 'weighted', 'centroid', 'median', 'ward']:
        for distance_metric in ['canberra', 'chebyshev', 'cityblock', 'euclidean', 'hamming', 'jaccard', 'matching', 'minkowski', 'rogerstanimoto', 'russellrao', 'seuclidean', 'sokalmichener', 'sokalsneath', 'sqeuclidean', 'yule']:
          if linkage_algorithm in ['centroid', 'median', 'ward'] and distance_metric != 'euclidean':
            continue

          desc = [str(num_ngrams_wanted), str(ngram_size) + 'part-gram', normalization_method, linkage_algorithm, distance_metric]
          print('testing ' + ' '.join(desc))
          generate_dendrogram(book_to_normalized_ngram_frequency, book_to_text.keys(), linkage_algorithm, distance_metric)
          if (check_dendrogram_valid()):
            #plt.show()
            save_dendrogram(desc)
          plt.close() # otherwise they stay open and consume all the memory
