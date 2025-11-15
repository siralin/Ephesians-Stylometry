from function_word_utils import calculate_raw_function_word_frequencies
import matplotlib.pyplot as plt
from general_plot_utils import get_label_color

# Displays a couple plots of words, comparing how frequently the various books use them.
def graph_paul_markers(book_to_text):
  colors = [get_label_color(b) for b in book_to_text.keys()]
  for word in  ['δε', 'τουτο']:
    frequencies = calculate_raw_function_word_frequencies(book_to_text, [word])

    fig = plt.figure(1, figsize=(8, 6))
    ax = fig.add_subplot()

    bars = zip(book_to_text.keys(), [f[0] for f in frequencies], colors)

    for x, y, color in sorted(bars, key=lambda x: x[1]):
      ax.bar(x, y, color=color)

    plt.xticks(rotation='vertical')
    plt.ylabel('Frequency of usage of ' + word)
    fig.tight_layout()
    plt.show()
    plt.close()