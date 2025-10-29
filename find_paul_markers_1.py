from read_text_utils import read_texts
from general_utils import SEPTUAGINT_BOOKS
from function_word_utils import calculate_normalized_function_word_frequencies, calculate_raw_function_word_frequencies
from scatter_plot_utils import generate_scatter_plot, generate_component_plot
from rearrange_texts_utils import merge_pauline_texts, merge_ignatian_texts
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA

wanted_septuagint_books = ['Epistle of Jeremiah']
excluded_nt_books = ['Matthew', 'Mark', 'Luke', 'John', 'Acts']
excluded_books = [b for b in SEPTUAGINT_BOOKS if b not in wanted_septuagint_books]
book_to_text = read_texts()
for ex_book in excluded_books + excluded_nt_books:
  book_to_text.pop(ex_book)

merge_pauline_texts(book_to_text)
merge_ignatian_texts(book_to_text)

# removed: 'κύριος', 'εἶπεν', 'ισραηλ', 'κυρίου', 'θεοῦ', 'γῆς', 'θεὸς', 'υἱοὶ', 'ἰδοὺ', 'δαυιδ', 'γῆν', 'υἱὸς', 'βασιλεὺς', 'λέγει', 'ιερουσαλημ', 'βασιλέως', 'υἱῶν', 'κυρίῳ', 'λέγων', 'ἡμέρας', 'ἐγένετο'
#function_words = ['καὶ', 'ἐν', 'τοῦ', 'ὁ', 'αὐτοῦ', 'εἰς', 'τὸν', 'τὴν', 'τὸ', 'τῷ', 'τῶν', 'δὲ', 'τῆς', 'σου', 'τὰ', 'ἐπὶ', 'οἱ', 'αὐτῶν', 'ὅτι', 'μου', 'ἡ', 'πρὸς', 'τῇ', 'οὐκ', 'τοὺς', 'μὴ', 'ἀπὸ', 'τοῖς', 'ἐκ', 'οὐ', 'αὐτῷ', 'ὡς', 'τὰς', 'αὐτὸν', 'γὰρ', 'ὑμῶν', 'αὐτῆς', 'κατὰ', 'με', 'αὐτοῖς', 'ἡμῶν', 'διὰ', 'μετὰ', 'αὐτοὺς', 'ἐστιν', 'ἐὰν', 'ἕως', 'ἐπ', 'πάντα', 'ἐγὼ', 'ἵνα', 'ἔσται', 'ὑμῖν', 'σε', 'ἢ', 'περὶ', 'τοῦτο', 'σοι', 'ταῖς', 'αἱ', 'εἰ', 'ἐξ', 'ἦν', 'μοι', 'ὑμᾶς', 'οὕτως', 'σὺ', 'οὖν', 'ταῦτα', 'ἐκεῖ', 'μετ', 'ἡμᾶς', 'αὐτόν', 'τί', 'ἀλλὰ', 'νῦν', 'ἔστιν', 'ἂν']

function_words = ['ἔστιν']

"""
Let us set the
percentage score for each of these ninety-nine words in Hutchinson’s shorter
verse against the ranked percentage scores for each of the other twenty-five
poets. Let us regard those where her score ranks in either the top six or the
bottom six – roughly the top and bottom quartiles – as ‘Hutchinson markers’
and see where these scores lead us.
"""

# TODO PROBLEM: shouldn't be outputting what it's outputting
def is_paul_marker(books_and_frequencies):
  sorted_books_and_frequencies = sorted(books_and_frequencies, key=lambda x: x[1])
  print('\t', sorted_books_and_frequencies)

  for i in range(1): # TODO BACK TO 5
    if sorted_books_and_frequencies[i][0] == 'Paul':
      return True
    elif sorted_books_and_frequencies[-i - 1][0] == 'Paul':
      return True

  return False

NORMALIZATION_METHOD = 'zscore'

# book_to_normalized_word_frequency: a 2d List[book index][word index]
# where the book index matches the index of the same book in book_to_word_counts and book_to_text
# and the word index matches the index of the same word in function_words.
book_to_normalized_word_frequency = calculate_raw_function_word_frequencies(
  book_to_text, function_words)

print(book_to_text.keys())
print(book_to_normalized_word_frequency)

books = list(book_to_text.keys())

paul_markers = []
for i, word in enumerate(function_words):
  books_and_frequencies = [(books[j], wf[i]) for (j, wf) in enumerate(book_to_normalized_word_frequency)]

  print(word, ':')
  if is_paul_marker(books_and_frequencies):
    paul_markers.append(word)

print('paul markers:', paul_markers)
