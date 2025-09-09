from delta_utils import read_normalized_texts, word_counts_to_zscores
from delta_plot_utils import display_graph
from pprint import pprint
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.decomposition import PCA
from collections import Counter
import math

NGRAM_SIZE = 3

# calculate frequency of every possible 2-gram in each book
book_to_chapter_to_text = read_normalized_texts()

books = {}
for book, chapter_to_text in book_to_chapter_to_text.items():
  book_text = ''
  for c in range(0, len(chapter_to_text)):
    book_text += chapter_to_text[c+1]
  books[book] = ''.join(book_text.split())

# we now have the text of each book, in order without spaces

book_to_ngram_counts = {}
total_ngram_counts = Counter()

for book, text in books.items():
  book_to_ngram_counts[book] = Counter()
  for i in range(0, len(text) - 1):
    ngram = text[i:i + NGRAM_SIZE]

    book_to_ngram_counts[book][ngram] += 1
    total_ngram_counts[ngram] += 1

zscores = word_counts_to_zscores(round(math.pow(24, NGRAM_SIZE)), book_to_ngram_counts, total_ngram_counts)
print(zscores)

display_graph(zscores, 0.7, -0.5)