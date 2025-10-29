from read_text_utils import read_texts
from general_utils import SEPTUAGINT_BOOKS
from function_word_utils import calculate_normalized_function_word_frequencies
from scatter_plot_utils import generate_scatter_plot, generate_component_plot
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA

"""
Generates Figures 2a and 2b for the thesis.
2a is the influence of the top 99 words on the two principal component vectors,
  excluding those which are obviously thematic.
2b is the results of arranging certain books (NT, a few Sept, and others)
  according to those vectors.
"""
wanted_septuagint_books = ['Epistle of Jeremiah']
excluded_nt_books = ['Matthew', 'Mark', 'Luke', 'John', 'Acts']
excluded_books = [b for b in SEPTUAGINT_BOOKS if b not in wanted_septuagint_books]
book_to_text = read_texts()
for ex_book in excluded_books + excluded_nt_books:
  book_to_text.pop(ex_book)

# removed: 'κύριος', 'εἶπεν', 'ισραηλ', 'κυρίου', 'θεοῦ', 'γῆς', 'θεὸς', 'υἱοὶ', 'ἰδοὺ', 'δαυιδ', 'γῆν', 'υἱὸς', 'βασιλεὺς', 'λέγει', 'ιερουσαλημ', 'βασιλέως', 'υἱῶν', 'κυρίῳ', 'λέγων', 'ἡμέρας', 'ἐγένετο'
function_words = ['και', 'εν', 'του', 'ο', 'αυτου', 'εις', 'τον', 'την', 'το', 'δε', 'τω', 'των', 'της', 'η', 'σου', 'τα', 'επι', 'οι', 'αυτων', 'οτι', 'μου', 'προς', 'τη', 'μη', 'ουκ', 'τους', 'ου', 'απο', 'αυτον', 'τοις', 'εκ', 'αυτω', 'εστιν', 'γαρ', 'ως', 'τας', 'αυτους', 'υμων', 'αυτης', 'κατα', 'αυτοις', 'με', 'ημων', 'σε', 'δια', 'μετα', 'εγω', 'ην', 'εαν', 'ει', 'παντα', 'σοι', 'εως', 'επ', 'ινα', 'εσται', 'τι', 'υμιν', 'εξ', 'αυτην', 'τουτο', 'αι', 'περι', 'αυτη', 'ταις', 'μοι', 'συ', 'υμας', 'ουτως', 'τις', 'ταυτα', 'ουν', 'παντες', 'εκει', 'μετ', 'αλλα', 'ημας']

NORMALIZATION_METHOD = 'zscore'

# book_to_normalized_word_frequency: a 2d List[book index][word index]
# where the book index matches the index of the same book in book_to_word_counts and book_to_text
# and the word index matches the index of the same word in function_words.
book_to_normalized_word_frequency = calculate_normalized_function_word_frequencies(
  book_to_text, function_words, NORMALIZATION_METHOD)

generate_component_plot(book_to_normalized_word_frequency, function_words, title="Figure 2a")
plt.show()

generate_scatter_plot(book_to_normalized_word_frequency, book_to_text.keys(), title="Figure 2b")
plt.show()
