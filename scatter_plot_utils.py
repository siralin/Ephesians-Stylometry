import pandas as pd
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from general_plot_utils import get_label_color

label_text = {
  '1 Corinthians': '1Cor',
  '1 John': '1John',
  '1 Peter': '1Pet',
  '1 Thessalonians': '1Thess',
  '1 Timothy': '1Tim',
  '2 Corinthians': '2Cor',
  '2 John': '2John',
  '2 Peter': '2Pet',
  '2 Thessalonians': '2Thess',
  '2 Timothy': '2Tim',
  '3 John': '3John',
  'Acts': 'Acts',
  'Colossians': 'Col',
  'Colossians parallel': 'CP',
  'Colossians unique': 'CU',
  'Ephesians': 'Eph',
  'Ephesians parallel': 'EphP',
  'Ephesians unique': 'EphU',
  'Galatians': 'Gal',
  'Hebrews': 'Heb',
  'James': 'James',
  'John': 'John',
  'Jude': 'Jude',
  'Luke': 'Luke',
  'Mark': 'Mark',
  'Matthew':'Matt',
  'Philemon': 'Philem',
  'Philippians': 'Phil',
  'Revelation': 'Rev',
  'Romans': 'Rom',
  'Titus': 'Titus'}

# Returns tuple of PCA, DataFrame
def do_pca(book_to_normalized_unit_frequency):
  data = pd.DataFrame(book_to_normalized_unit_frequency)
  return PCA(n_components=2, svd_solver='full').fit(data), data

# Generates a scatter plot of the given units aligned to the two PCA vectors
# to illustrate how each unit contributes to each vector.
# To display the plot, call plt.show().
#
# book_to_normalized_unit_frequency: a 2d List[book index][unit index]
# where the unit index matches the index in the given units
# units: List of units
def generate_component_plot(book_to_normalized_unit_frequency, units):
  pca, _ = do_pca(book_to_normalized_unit_frequency)

  # There are two 'components' arrays, each with one element per unit
  # We can graph them to see how important each unit is to the PCA.

  unique_figure_id = 2
  fig = plt.figure(unique_figure_id, figsize=(8, 6))
  ax = fig.add_subplot()

  scatter = ax.scatter(
    pca.components_[0],
    pca.components_[1],
  )

  for i, unit in enumerate(units):
    ax.annotate(unit, (pca.components_[0][i], pca.components_[1][i]))

  variance = pca.explained_variance_ratio_
  ax.set_xlabel('Vector A (' + to_percent(variance[0]) + ')')
  ax.set_ylabel('Vector B (' + to_percent(variance[1]) + ')')
  fig.tight_layout()

def to_percent(decimal):
  return f"{decimal:.0%}"

# Generates a scatter plot of the given books with their unit data compressed into two dimensions.
# Returns nothing.
# To display the plot, call plt.show().
#
# book_to_normalized_unit_frequency: a 2d List[book index][unit index]
# where the book index matches the index of the same book in the given books
# books: List of book titles
def generate_scatter_plot(book_to_normalized_unit_frequency, books, title=None):
  pca, data = do_pca(book_to_normalized_unit_frequency)

  unique_figure_id = 1
  fig = plt.figure(unique_figure_id, figsize=(8, 6))
  ax = fig.add_subplot()

  X_reduced = pca.transform(data)
  scatter = ax.scatter(
      X_reduced[:, 0],
      X_reduced[:, 1],
      c = [get_label_color(book) for book in books]
  )

  for i, book in enumerate(books):
    ax.annotate(label_text.get(book, book), (X_reduced[i, 0], X_reduced[i, 1]))

  plt.gca().update({"title":title})
  fig.tight_layout()