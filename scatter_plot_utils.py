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

# Generates a scatter plot of the given books with their unit data compressed into two dimensions.
# Returns nothing.
# To display the plot, call plt.show().
#
# book_to_normalized_unit_frequency: a 2d List[book index][unit index]
# where the book index matches the index of the same book in the given books
# books: List of book titles
def generate_scatter_plot(book_to_normalized_unit_frequency, books, title=None):
  data = pd.DataFrame(book_to_normalized_unit_frequency)

  unique_figure_id = 1
  fig = plt.figure(unique_figure_id, figsize=(8, 6))
  ax = fig.add_subplot()

  X_reduced = PCA(n_components=2,svd_solver='full').fit_transform(data)
  scatter = ax.scatter(
      X_reduced[:, 0],
      X_reduced[:, 1],
      c = [get_label_color(book) for book in books]
  )

  for i, book in enumerate(books):
    ax.annotate(label_text[book], (X_reduced[i, 0], X_reduced[i, 1]))

  plt.gca().update({"title":title})
  fig.tight_layout()