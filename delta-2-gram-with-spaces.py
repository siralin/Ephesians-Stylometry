from delta_utils import read_normalized_texts, word_counts_to_zscores
from delta_plot_utils import display_graph
from pprint import pprint
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.decomposition import PCA
from collections import Counter
import math

NGRAM_SIZE = 2

# TODO double check I've divided Eph and Col properly into parallel & unique sets

# calculate frequency of every possible 2-gram in each book
book_to_chapter_to_text = read_normalized_texts()

del book_to_chapter_to_text['colossiansunique']
del book_to_chapter_to_text['colossiansparallel']
del book_to_chapter_to_text['ephesiansunique']
del book_to_chapter_to_text['ephesiansparallel']

# (Note that if you don't delete either the originals or the parallel/unique texts,
# you get incorrect information about the most common words/bigrams/etc)

books = {}
for book, chapter_to_text in book_to_chapter_to_text.items():
  book_text = ' '
  for c in range(0, len(chapter_to_text)):
    book_text += chapter_to_text[c+1] + ' '
  books[book] = book_text

# Solved the problem of joining words (in unique/parallel texts) that had whole verses between them
# by leaving the spaces in.

# we now have the text of each book, in order.
for book, text in books.items():
  print(book, len(text))

book_to_ngram_counts = {}
total_ngram_counts = Counter()

for book, text in books.items():
  book_to_ngram_counts[book] = Counter()
  for i in range(0, len(text) - 1):
    ngram = text[i:i + NGRAM_SIZE]

    book_to_ngram_counts[book][ngram] += 1
    total_ngram_counts[ngram] += 1

    # can remove ngrams containing spaces if you want
    """
    if " " not in ngram:
      book_to_ngram_counts[book][ngram] += 1
      total_ngram_counts[ngram] += 1
    """

zscores = word_counts_to_zscores(round(math.pow(25, NGRAM_SIZE)), book_to_ngram_counts, total_ngram_counts)

display_graph(zscores, 0.3, -0.2)