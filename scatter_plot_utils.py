import pandas as pd
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from general_plot_utils import get_label_color

label_text = {
  '1 Corinthians': '1C',
  '1 John': '1J',
  '1 Peter': '1P',
  '1 Thessalonians': '1Th',
  '1 Timothy': '1Ti',
  '2 Corinthians': '2C',
  '2 John': '2J',
  '2 Peter': '2P',
  '2 Thessalonians': '2Th',
  '2 Timothy': '2Ti',
  '3 John': '3J',
  'Acts': 'A',
  'Colossians': 'C',
  'Colossians parallel': 'CP',
  'Colossians unique': 'CU',
  'Ephesians': 'E',
  'Ephesians parallel': 'EP',
  'Ephesians unique': 'EU',
  'Galatians': 'G',
  'Hebrews': 'H',
  'James': 'Ja',
  'John': 'Jo',
  'Jude': 'Ju',
  'Luke': 'L',
  'Mark': 'Mar',
  'Matthew':'Mat',
  'Philemon': 'Phile',
  'Philippians': 'Phili',
  'Revelation': 'Re',
  'Romans': 'Ro',
  'Titus': 'T'}

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