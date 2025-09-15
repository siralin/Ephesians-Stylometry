import pandas as pd
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from general_utils import UNCONTESTED_PAUL_BOOKS, CONTESTED_PAUL_BOOKS
from scipy.cluster.hierarchy import dendrogram, linkage

# book_to_bigram_to_norm_freq: list of lists
#  where book_to_bigram_to_norm_freq[0] gets you all the bigram frequencies for the first book
# book_titles: list of titles in the same order as book_to_bigram_to_norm_freq
def display_dendrogram(book_to_bigram_to_norm_freq, book_titles, linkage_algorithm, distance_metric):
  generate_dendrogram(book_to_bigram_to_norm_freq, book_titles, linkage_algorithm, distance_metric)

  #filename = '-'.join(['dendrogram', str(ngram_size) + 'gram', str(num_bigrams_wanted), linkage_algorithm, distance_metric])
  #plt.savefig(filename + '.png', format='png', dpi=100)
  plt.show()

# Generates but does not display dendrogram.
# Use plt.show() to display it
# or plt.gca() to get its Axes and modify or analyze it.
# Returns nothing.
#
# book_to_bigram_to_norm_freq: list of lists
#  where book_to_bigram_to_norm_freq[0] gets you all the bigram frequencies for the first book
# book_titles: list of titles in the same order as book_to_bigram_to_norm_freq
def generate_dendrogram(book_to_bigram_to_norm_freq, book_titles, linkage_algorithm, distance_metric):
  try:
    Z = linkage(book_to_bigram_to_norm_freq, method=linkage_algorithm, metric=distance_metric)
  except ValueError as exc:
    print(book_to_bigram_to_norm_freq)
    raise RuntimeError from exc

  plt.figure(figsize=(10, 4))
  plt.title('Hierarchical Clustering Dendrogram (Bigrams)')
  plt.xlabel('text number')
  plt.ylabel('distance')
  dendrogram(
             Z,
             leaf_rotation=90.,  # rotates the x axis labels
             leaf_font_size=8.,  # font size for the x axis labels
             labels=book_titles)

  ax = plt.gca()
  x_labels = ax.get_xmajorticklabels()
  for x in x_labels:
    x.set_color(get_label_color(x.get_text()))

# A valid dendrogram groups all of paul's uncontested books together without any of
# those books that definitely aren't his in between.
def check_dendrogram_valid():
  ax = plt.gca()
  x_label_colors = [x.get_color() for x in ax.get_xmajorticklabels()]
  return check_dendrogram_labels_valid(x_label_colors)

def check_dendrogram_labels_valid(label_colors):
  num_paul_books = 0
  for color in label_colors:
    if color == 'blue':
      num_paul_books += 1
      if num_paul_books == len(UNCONTESTED_PAUL_BOOKS):
        return True
    elif color == 'green':
      if num_paul_books > 0:
        return num_paul_books == len(UNCONTESTED_PAUL_BOOKS)
    elif color != 'red':
      raise RuntimeError("didn't expect label color " + color)

  raise RuntimeError("dendrogram appears to be missing labels")

# book_to_word_zscores: dictionary of book title to dictionary of word/ngram to its zscore.
def display_graph(book_to_word_zscores, label_x_adjustment, label_y_adjustment, title=""):

  # create DataFrame from dictionary
  # where keys are Greek words and values are
  # the z-scores (consistently ordered)
  word_to_zscores = {}
  labels = []
  colors = []
  for book, word_zscores in book_to_word_zscores.items(): # note dicts are insertion-ordered
    for word, zscore in word_zscores.items():
      if word not in word_to_zscores:
        word_to_zscores[word] = []
      word_to_zscores[word].append(zscore)
    labels.append(book)

    colors.append(get_label_color(book))

  # DataFrame column order follows dict insertion order
  data = pd.DataFrame(word_to_zscores)

  fig = plt.figure(1, figsize=(8, 6))
  ax = fig.add_subplot(111)

  X_reduced = PCA(n_components=2).fit_transform(data)
  scatter = ax.scatter(
      X_reduced[:, 0],
      X_reduced[:, 1],
      c = colors
  )
  plt.gca().update(dict(title=title))

  for i, label in enumerate(labels):
    ax.annotate(label, (X_reduced[i, 0] + label_x_adjustment, X_reduced[i, 1] + label_y_adjustment))

  plt.show()

def get_label_color(label_text):
  if label_text in UNCONTESTED_PAUL_BOOKS:
    return "blue"
  elif label_text in CONTESTED_PAUL_BOOKS:
    return "red"
  else:
    return "green"
