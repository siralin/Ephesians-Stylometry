import os
from collections import Counter
from statistics import stdev, fmean
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.decomposition import PCA

# convert frequency to z-score (the number of standard deviations above/below the mean)
# this means that over the whole corpus,
# the mean for each word is 0 and the standard deviation is 1
#
# words: list of all the words we're interested in
# text_to_word_frequencies: dictionary of text title -> dictionary of word to frequency within text
#   (as a proportion of all words in that text).  May include words we're not interested in.
def normalize_frequencies_to_zscore(words, text_to_word_frequencies):
  word_to_mean = {}
  word_to_sd = {}
  for word in words:
    frequencies = [f[word] for f in text_to_word_frequencies.values()]
    word_to_mean[word] = fmean(frequencies)
    word_to_sd[word] = stdev(frequencies)

  book_to_word_zscores = {}
  for book, frequencies in text_to_word_frequencies.items():
    book_to_word_zscores[book] = {}
    for word, mean in word_to_mean.items():
      zscore = (frequencies[word] - mean) / word_to_sd[word]
      book_to_word_zscores[book][word] = zscore

  return book_to_word_zscores

# book_to_word_zscores: dictionary of text title to dictionary of word to its z-score
# returns dictionary of text title to
#     dictionary of other text title to manhattan distance between their z-scores
def calculate_text_manhattan_distances(book_to_word_zscores):
  manhattan_distances = {}
  for book, word_to_zscore in book_to_word_zscores.items():
    manhattan_distances[book] = {}
    for other_book, other_word_to_zscore in book_to_word_zscores.items():
      sum = 0.0
      for word, zscore in word_to_zscore.items():
        sum += abs(zscore - other_word_to_zscore[word])
      manhattan_distances[book][other_book] = sum
  return manhattan_distances

# get the counts for each book for just the overall most frequent words
def find_book_to_word_frequencies(book_to_word_counts, most_frequent_words):
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

# returns a dictionary of book name
#   to dictionary of chapter number to text of that chapter
def read_texts():

  DIRECTORY = 'netbible_chapters'
  NORMALIZED_FILE_SUFFIX = '-norm'

  book_to_chapter_to_text = {}

  for filename in os.listdir(DIRECTORY):
    if NORMALIZED_FILE_SUFFIX in filename:
      book_chapter_hyphen_index = filename.index('-', 2)
      book = filename[:book_chapter_hyphen_index]
      post_chapter_hyphen_index = filename.index('-', book_chapter_hyphen_index + 1)
      chapter = filename[book_chapter_hyphen_index + 1:post_chapter_hyphen_index]

      if book not in book_to_chapter_to_text:
        book_to_chapter_to_text[book] = {}

      chapter_contents = ''
      with open(os.path.join(DIRECTORY, filename), 'r') as handle:
        for line in handle:
          chapter_contents += line
      book_to_chapter_to_text[book][int(chapter)] = chapter_contents

  return book_to_chapter_to_text

# reads in the netbible chapter texts and
# returns a dictionary of book name
#   to dictionary of word to z-score (normalized frequency)
def read_and_calculate_text_to_zscores(num_most_frequent_words):

  DIRECTORY = 'netbible_chapters'
  NORMALIZED_FILE_SUFFIX = '-norm'

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
  return word_counts_to_zscores(num_most_frequent_words, book_to_word_counts, total_word_counts)

# using the given word count dicts,
# returns a dictionary of book name
#   to dictionary of word to z-score (normalized frequency)
def word_counts_to_zscores(num_most_frequent_words, book_to_word_counts, total_word_counts):
  # we have a list of words
  most_frequent_words = [x[0] for x in total_word_counts.most_common(num_most_frequent_words)]

  # we have a dictionary of dictionaries
  book_to_word_frequencies = find_book_to_word_frequencies(book_to_word_counts, most_frequent_words)

  # we have a dictionary of dictionaries
  return normalize_frequencies_to_zscore(most_frequent_words, book_to_word_frequencies)

def display_graph(book_to_word_zscores, label_x_adjustment, label_y_adjustment):

  # create DataFrame from dictionary
  # where keys are Greek words and values are
  # the z-scores (consistently ordered)
  word_to_zscores = {}
  labels = [] # TODO make sure labels accurate
  colors = []
  for book, word_zscores in book_to_word_zscores.items(): # note dicts are insertion-ordered
    for word, zscore in word_zscores.items():
      if word not in word_to_zscores:
        word_to_zscores[word] = []
      word_to_zscores[word].append(zscore)
    labels.append(book)

    if book in ["romans", "1-corinthians", "2-corinthians", "galatians", "philippians", "1-thessalonians", "philemon"]:
      colors.append("b")
    elif book in ["ephesians", "colossians", "2-thessalonians", "1-timothy", "2-timothy", "titus"]:
      colors.append("r")
    else:
      colors.append("g")

  # DataFrame column order follows dict insertion order
  data = pd.DataFrame(word_to_zscores)

  fig = plt.figure(1, figsize=(8, 6))
  ax = fig.add_subplot(111)

  X_reduced = PCA(n_components=2).fit_transform(data)
  scatter = ax.scatter(
      X_reduced[:, 0],
      X_reduced[:, 1],
      c = colors
  )

  for i, label in enumerate(labels):
    ax.annotate(label, (X_reduced[i, 0] + label_x_adjustment, X_reduced[i, 1] + label_y_adjustment))

  plt.show()
