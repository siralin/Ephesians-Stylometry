import matplotlib.pyplot as plt
from general_utils import BOOK_NAMES, UNCONTESTED_PAUL_BOOKS
from scipy.cluster.hierarchy import dendrogram, linkage
from general_plot_utils import get_label_color

# Generates a dendrogram for the given data.
# Use plt.show() to display it
# or plt.gca() to get its Axes and modify or analyze it.
#
# book_to_normalized_unit_frequency: a 2d List[book index][unit index]
#   where the book index matches the index of the same book in book_titles
#   and the unit indexes match across books
# book_titles: Iterable of book titles
#
# Returns a dictionary of data computed to render the dendrogram,
# containing keys 'color_list', 'icoord', 'dcoord', 'ivl', 'leaves', and 'leaves_color_list'.
def generate_dendrogram(book_to_normalized_unit_frequency, book_titles, linkage_algorithm, distance_metric, title="Hierarchical Clustering Dendrogram"):
  Z = linkage(book_to_normalized_unit_frequency, method=linkage_algorithm, metric=distance_metric)

  fig = plt.figure(figsize=(8, 6))
  plt.title(title)
  plt.xlabel('Book')
  plt.ylabel('Distance')
  dendrogram_data_structures = dendrogram(
    Z,
    leaf_rotation=90,  # rotates the x axis labels
    leaf_font_size=8,  # font size for the x axis labels
    labels = list(book_titles))

  ax = plt.gca()
  x_labels = ax.get_xmajorticklabels()
  for x in x_labels:
    x.set_color(get_label_color(x.get_text()))

  fig.tight_layout()
  return dendrogram_data_structures # TODO check whether leaf colors actually got updated

def _check_dendrogram_labels_valid(label_colors, books = BOOK_NAMES):
  expected_paul_books = len(set(books) & set(UNCONTESTED_PAUL_BOOKS))

  num_paul_books = 0
  for color in label_colors:
    if color == 'blue':
      num_paul_books += 1
      if num_paul_books == expected_paul_books:
        return True
    elif color == 'green':
      if num_paul_books > 0:
        return num_paul_books == expected_paul_books
    elif color != 'red':
      raise RuntimeError("didn't expect label color " + color)

  raise RuntimeError("dendrogram appears to be missing labels")
