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
  'Ephesians': 'Eph',
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
  'Titus': 'Titus',
  'Paul': 'Paul',
  'Ignatius': 'Ign',
  'Clement 1 Corinthians': 'Clem1Cor',
  'Clement 2 Corinthians': 'Clem2Cor',
  'Barnabas': 'Bar',
  'Didache': 'Did',
  'Diognetus': 'Dio',
  'Hermas Shepherd': 'Hermas',
  'Ignatius Ephesians': 'IgEph',
  'Ignatius Magnesians': 'Mag',
  'Ignatius Philadelphians': 'IgPhil',
  'Ignatius Polycarp': 'IgPoly',
  'Ignatius Romans': 'IgRom',
  'Ignatius Smyrnaeans': 'Smy',
  'Ignatius Trallians': 'Tra',
  'Iranaeus Martyrdom Polycarp': 'IrMartyr',
  'Epistle of Jeremiah': 'Jer'}

# Returns tuple of PCA, DataFrame
def do_pca(book_to_normalized_unit_frequency):
  data = pd.DataFrame(book_to_normalized_unit_frequency)
  return PCA(n_components=2, svd_solver='full').fit(data), data

def to_percent(decimal):
  return f"{decimal:.0%}"

# Generates a scatter plot of the given books with their unit data compressed into two dimensions.
# Returns nothing.
# To display the plot, call plt.show().
#
# book_to_normalized_unit_frequency: a 2d List[book index][unit index]
# where the book index matches the index of the same book in the given books
# books: List of book titles
def generate_scatter_plot(book_to_normalized_unit_frequency, books, title=None, include_labels=True, base_xy=(0,0), xy_adjustments={}, figsize=(8,6)):
  pca, data = do_pca(book_to_normalized_unit_frequency)

  unique_figure_id = 1
  fig = plt.figure(unique_figure_id, figsize=figsize)
  ax = fig.add_subplot()

  X_reduced = pca.transform(data)
  scatter = ax.scatter(
      X_reduced[:, 0],
      X_reduced[:, 1],
      c = [get_label_color(book) for book in books]
  )

  if include_labels:
    for i, book in enumerate(books):
      x = X_reduced[i, 0] + base_xy[0] + xy_adjustments.get(book, (0, 0))[0]
      y = X_reduced[i, 1] + base_xy[1] + xy_adjustments.get(book, (0, 0))[1]

      book_name = book
      book_suffix = ''
      if book.endswith(('A', 'B', 'C', 'D')):
        book_name = book[:-2]
        book_suffix = book[-2:]
      ax.annotate(label_text.get(book_name, book) + book_suffix, (x, y))

  variance = pca.explained_variance_ratio_
  ax.set_xlabel('Vector A (' + to_percent(variance[0]) + ')')
  ax.set_ylabel('Vector B (' + to_percent(variance[1]) + ')')

  plt.gca().update({"title":title})
  fig.tight_layout()