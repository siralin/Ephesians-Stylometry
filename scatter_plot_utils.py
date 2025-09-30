import pandas as pd
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from general_plot_utils import get_label_color

label_text = {
  '1 corinthians': '1C',
  '1 john': '1J',
  '1 peter': '1P',
  '1 thessalonians': '1Th',
  '1 timothy': '1Ti',
  '2 corinthians': '2C',
  '2 john': '2J',
  '2 peter': '2P',
  '2 thessalonians': '2Th',
  '2 timothy': '2Ti',
  '3 john': '3J',
  'acts': 'A',
  'colossians': 'C',
  'colossians parallel': 'CP',
  'colossians unique': 'CU',
  'ephesians': 'E',
  'ephesians parallel': 'EP',
  'ephesians unique': 'EU',
  'galatians': 'G',
  'hebrews': 'H',
  'james': 'Ja',
  'john': 'Jo',
  'jude': 'Ju',
  'luke': 'L',
  'mark': 'Mar',
  'matthew':'Mat',
  'philemon': 'Phile',
  'philippians': 'Phili',
  'revelation': 'Re',
  'romans': 'Ro',
  'titus': 'T'}

# Generates a scatter plot of the given books with their unit data compressed into two dimensions.
# Returns nothing.
# To display the plot, call plt.show().
#
# book_to_normalized_unit_frequency: a 2d List[book index][unit index]
# where the book index matches the index of the same book in the given books
# books: List of book titles
def generate_scatter_plot(book_to_normalized_unit_frequency, books):
  data = pd.DataFrame(book_to_normalized_unit_frequency)

  unique_figure_id = 1
  fig = plt.figure(unique_figure_id, figsize=(8, 6))
  ax = fig.add_subplot()

  X_reduced = PCA(n_components=2).fit_transform(data)
  scatter = ax.scatter(
      X_reduced[:, 0],
      X_reduced[:, 1],
      c = [get_label_color(book) for book in books]
  )

  for i, book in enumerate(books):
    ax.annotate(label_text[book], (X_reduced[i, 0], X_reduced[i, 1]))

  fig.tight_layout()