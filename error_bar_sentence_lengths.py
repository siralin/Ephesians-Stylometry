import matplotlib.pyplot as plt
import numpy as np
from sentence_length_utils import read_sentence_lengths
from statistics import stdev, fmean
from general_plot_utils import get_label_color
from general_utils import BOOK_NAMES

unsorted_book_to_sentence_lengths = read_sentence_lengths()

book_to_sentence_lengths = dict([(b, unsorted_book_to_sentence_lengths[b]) for b in BOOK_NAMES])
xs = np.array(list(book_to_sentence_lengths.keys()))
ys = np.array([fmean(lengths) for lengths in book_to_sentence_lengths.values()])
es = np.array([stdev(lengths) for lengths in book_to_sentence_lengths.values()])
colors = [get_label_color(book) for book in book_to_sentence_lengths]

unique_figure_id = 1
fig = plt.figure(unique_figure_id, figsize=(8, 6))
ax = fig.add_subplot()

for x, y, err, color in zip(xs, ys, es, colors):
  ax.errorbar(x, y, err, capsize=5, capthick=2, color=color, marker='o')

plt.xticks(rotation='vertical')
fig.tight_layout()
plt.show()