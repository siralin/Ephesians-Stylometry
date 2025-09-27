import os
from read_text_utils import read_normalized_texts
from ngram_utils import calculate_normalized_ngram_frequencies
from scatter_plot_utils import generate_scatter_plot
import matplotlib.pyplot as plt

generation_specs = set()

for filename in os.listdir('ngram-candidates'):
  specs = filename.split('-')

  num_ngrams_wanted = int(specs[1])
  ngram_size = int(specs[2][0])
  merge_words = specs[3] == 'True'
  normalization_method = specs[4]

  generation_specs.add((num_ngrams_wanted, ngram_size, merge_words, normalization_method))

for num_ngrams_wanted, ngram_size, merge_words, normalization_method in generation_specs:
  book_to_text = read_normalized_texts()
  if merge_words:
    for book, text in book_to_text.items():
      book_to_text.update({book: "".join(text.split())})

  book_to_normalized_ngram_frequency, ngrams = calculate_normalized_ngram_frequencies(
    book_to_text, num_ngrams_wanted, ngram_size, normalization_method)

  desc = [str(num_ngrams_wanted), str(ngram_size) + 'gram', str(merge_words), normalization_method]
  print('testing ' + ' '.join(desc))

  generate_scatter_plot(book_to_normalized_ngram_frequency, book_to_text.keys())
  plt.show()