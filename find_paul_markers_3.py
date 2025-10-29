from read_text_utils import read_texts
from general_utils import SEPTUAGINT_BOOKS
from function_word_utils import calculate_normalized_function_word_frequencies
from scatter_plot_utils import generate_scatter_plot, generate_component_plot
from rearrange_texts_utils import rearrange_pauline_texts, merge_colossians_ephesians_texts
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA

"""
Generates Figures 5a and 5b for the thesis.
5a is the influence of the top Paul markers on the two principal component vectors,
5b is the results of arranging certain books (NT, a few Sept, and others)
  according to those vectors.
"""
wanted_septuagint_books = ['Epistle of Jeremiah']
excluded_nt_books = ['Matthew', 'Mark', 'Luke', 'John', 'Acts']
excluded_books = [b for b in SEPTUAGINT_BOOKS if b not in wanted_septuagint_books]
book_to_text = read_texts()
for ex_book in excluded_books + excluded_nt_books:
  book_to_text.pop(ex_book)

# get rid of uselessly short books?
for book in set(book_to_text.keys()):
  if book not in ['Ephesians', 'Colossians'] and book_to_text[book].count(' ') < 1999:
    book_to_text.pop(book)

#rearrange_pauline_texts(book_to_text)
#merge_colossians_ephesians_texts(book_to_text) #not useful

function_words = ['και', 'το', 'δε', 'τω', 'η', 'οτι', 'μου', 'ου', 'γαρ', 'τας', 'εγω', 'ην', 'ει', 'τι', 'υμας', 'ουτως', 'παντες', 'αλλα']

NORMALIZATION_METHOD = 'zscore'

# book_to_normalized_word_frequency: a 2d List[book index][word index]
# where the book index matches the index of the same book in book_to_word_counts and book_to_text
# and the word index matches the index of the same word in function_words.
book_to_normalized_word_frequency = calculate_normalized_function_word_frequencies(
  book_to_text, function_words, NORMALIZATION_METHOD)

generate_component_plot(book_to_normalized_word_frequency, function_words, title="Figure 5a")
plt.show()

generate_scatter_plot(book_to_normalized_word_frequency, book_to_text.keys(), title="Figure 5b")
plt.show()
