from function_word_utils import calculate_raw_function_word_frequencies
from read_text_utils import read_texts
from general_utils import SEPTUAGINT_BOOKS
import matplotlib.pyplot as plt
from general_plot_utils import get_label_color
from rearrange_texts_utils import add_merged_pauline_text

#WORD = 'καὶ'

wanted_septuagint_books = ['Epistle of Jeremiah']
excluded_nt_books = ['Matthew', 'Mark', 'Luke', 'John', 'Acts']
excluded_books = [b for b in SEPTUAGINT_BOOKS if b not in wanted_septuagint_books]
book_to_text = read_texts()
for ex_book in excluded_books + excluded_nt_books:
  book_to_text.pop(ex_book)

add_merged_pauline_text(book_to_text)

colors = [get_label_color(b) for b in book_to_text.keys()]

# from top 110, paul in top/bottom 7
for WORD in  ['και', 'αυτου', 'εις', 'το', 'δε', 'τω', 'των', 'η', 'οτι', 'μου', 'ουκ', 'ου', 'γαρ', 'τας', 'εγω', 'ην', 'ει', 'τι', 'εξ', 'τουτο', 'περι', 'μοι', 'υμας', 'ουτως', 'τις', 'παντες', 'αλλα', 'αν', 'ος']:
  frequencies = calculate_raw_function_word_frequencies(book_to_text, [WORD])

  fig = plt.figure(1, figsize=(8, 6))
  ax = fig.add_subplot()

  bars = zip(book_to_text.keys(), [f[0] for f in frequencies], colors)

  for x, y, color in sorted(bars, key=lambda x: x[1]):
    ax.bar(x, y, color=color)

  plt.xticks(rotation='vertical')
  plt.ylabel('Frequency of usage of ' + WORD)
  fig.tight_layout()
  plt.show()