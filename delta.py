import os
from collections import Counter
from delta_utils import normalize_frequencies_to_zscore, calculate_text_manhattan_distances
from pprint import pprint
import matplotlib.pyplot as plt
import numpy as np

DIRECTORY = 'netbible_chapters'
NORMALIZED_FILE_SUFFIX = '-norm'
NUM_MOST_FREQUENT_WORDS = 2

book_to_word_counts = {}
total_word_counts = Counter()

# count all words in each book and overall
for filename in os.listdir(DIRECTORY):
  if NORMALIZED_FILE_SUFFIX in filename:
    book = filename[:filename.index('-', 2)]
    if book not in book_to_word_counts:
      book_to_word_counts[book] = Counter()

    with open(os.path.join(DIRECTORY, filename), 'r') as handle:
      for line in handle:
        words = line.split()
        for word in words:
          book_to_word_counts[book][word] += 1
          total_word_counts[word] += 1

# we have a list of words
most_frequent_words = [x[0] for x in total_word_counts.most_common(NUM_MOST_FREQUENT_WORDS)]

# get the counts for each book for just the overall most frequent words
def find_book_to_word_frequencies():
  book_to_frequent_word_counts = {}
  for book in book_to_word_counts.keys():
    book_to_frequent_word_counts[book] = {}
    for word in most_frequent_words:
      book_to_frequent_word_counts[book][word] = book_to_word_counts[book][word]

  # transform the counts to frequencies
  # result: a dictionary of book title string to
  #   dictionary of word string to frequency number
  book_to_word_frequencies = {}
  for book in book_to_word_counts.keys():
    book_to_word_frequencies[book] = {}
    num_words_in_book = sum(book_to_word_counts[book].values())
    for word, count in book_to_frequent_word_counts[book].items():
      book_to_word_frequencies[book][word] = count / num_words_in_book

  return book_to_word_frequencies

# we have a dictionary of dictionaries
book_to_word_frequencies = find_book_to_word_frequencies()

# we have a dictionary of dictionaries
book_to_word_zscores = normalize_frequencies_to_zscore(most_frequent_words, book_to_word_frequencies)
pprint(book_to_word_zscores)

xpoints = []
ypoints = []
for book, zscores in book_to_word_zscores.items():
  xpoints.add(zscores['και'])
  ypoints.add(zscores['ο'])
  print(book + ',' + str(zscores['και']) + ',' + str(zscores['ο']))

plt.plot(np.array(xpoints), np.array(ypoints))
plt.show()

manhattan_distances = calculate_text_manhattan_distances(book_to_word_zscores)
#pprint(manhattan_distances)

# TODO print more nicely, maybe in a grid
# TODO unit tests of functions


