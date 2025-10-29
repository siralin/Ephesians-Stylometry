from function_word_utils import calculate_raw_function_word_frequencies
from read_text_utils import read_texts
from general_utils import SEPTUAGINT_BOOKS
import matplotlib.pyplot as plt
from general_plot_utils import get_label_color

#WORD = 'καὶ'

wanted_septuagint_books = ['Epistle of Jeremiah']
excluded_nt_books = ['Matthew', 'Mark', 'Luke', 'John', 'Acts']
excluded_books = [b for b in SEPTUAGINT_BOOKS if b not in wanted_septuagint_books]
book_to_text = read_texts()
for ex_book in excluded_books + excluded_nt_books:
  book_to_text.pop(ex_book)

colors = [get_label_color(b) for b in book_to_text.keys()]

# eph/col interesting: ἐν, τοῦ
#interesting: 'τὰς', 'γὰρ',
#['καὶ', 'ἐν', 'τοῦ', 'ὁ', 'αὐτοῦ', 'εἰς', 'τὸν', 'τὴν', 'τὸ', 'τῷ', 'τῶν', 'δὲ', 'τῆς', 'τὰ', 'ἐπὶ', 'οἱ', 'αὐτῶν', 'ὅτι', 'πρὸς', 'τῇ', 'οὐκ', 'τοὺς', 'μὴ', 'ἀπὸ', 'τοῖς', 'ἐκ', 'οὐ', 'αὐτῷ', 'ὡς', 'τὰς', 'γὰρ', 'ὑμῶν', 'κατὰ', 'ἡμῶν', 'διὰ', 'μετὰ', 'ἐστιν', 'ἵνα', 'περὶ', 'τοῦτο', 'ταῖς', 'οὖν', 'ταῦτα', 'ἀλλὰ', 'νῦν']

for WORD in ['ἀλλὰ']:#['καὶ', 'ἐν', 'τοῦ', 'αὐτοῦ', 'εἰς', 'τὸν', 'τῶν', 'τῆς', 'οἱ', 'ὅτι', 'τῇ', 'οὐκ', 'μὴ', 'ἐκ', 'διὰ', 'ἀλλὰ']:
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