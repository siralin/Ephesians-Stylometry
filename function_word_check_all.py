from function_word_utils import calculate_normalized_function_word_frequencies, FUNCTION_WORDS
from read_nt_text_utils import read_normalized_texts
from dendrogram_utils import generate_dendrogram, check_dendrogram_valid, save_dendrogram
import matplotlib.pyplot as plt

book_to_text = read_normalized_texts()

for num_words_wanted in range(1, len(FUNCTION_WORDS) + 1):
  function_words = FUNCTION_WORDS[:num_words_wanted]

  for normalization_method in ['simple', 'zscore']:
    book_to_normalized_word_frequency = calculate_normalized_function_word_frequencies(
      book_to_text, function_words, normalization_method)

    for linkage_algorithm in ['complete', 'average', 'weighted', 'centroid', 'median', 'ward']:
      for distance_metric in ['canberra', 'chebyshev', 'cityblock', 'euclidean', 'hamming', 'jaccard', 'matching', 'minkowski', 'rogerstanimoto', 'russellrao', 'seuclidean', 'sokalmichener', 'sokalsneath', 'sqeuclidean', 'yule']:
        if linkage_algorithm in ['centroid', 'median', 'ward'] and distance_metric != 'euclidean':
          continue

        desc = [str(num_words_wanted), 'function-words', normalization_method, linkage_algorithm, distance_metric]
        print('testing ' + ' '.join(desc))
        generate_dendrogram(book_to_normalized_word_frequency, book_to_text.keys(), linkage_algorithm, distance_metric)
        if (check_dendrogram_valid()):
          #plt.show()
          save_dendrogram(desc)
        plt.close() # otherwise they stay open and consume all the memory
