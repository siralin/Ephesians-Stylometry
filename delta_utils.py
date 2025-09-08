import os
from collections import Counter
from statistics import stdev, fmean
from general_utils import UNCONTESTED_PAUL_BOOKS, CONTESTED_PAUL_BOOKS

# convert frequency to z-score (the number of standard deviations above/below the mean)
# this means that over the whole corpus,
# the mean for each word is 0 and the standard deviation is 1
#
# words: list of all the words we're interested in
# title_to_word_frequencies: dictionary of text title -> dictionary of word to frequency within text
#   (as a proportion of all words in that text).  May include words we're not interested in.
#   May or may not contain entries for frequencies of 0.
#
# returns a dict of the title_to_word_frequencies keys to their normalized zscores
def normalize_frequencies_to_zscore(words, title_to_word_frequencies):
  word_to_mean = {}
  word_to_sd = {}
  for word in words:
    frequencies = [f.get(word, 0) for f in title_to_word_frequencies.values()]
    word_to_mean[word] = fmean(frequencies)
    word_to_sd[word] = stdev(frequencies)

  book_to_word_zscores = {}
  for book, frequencies in title_to_word_frequencies.items():
    book_to_word_zscores[book] = {}
    for word, mean in word_to_mean.items():
      zscore = (frequencies.get(word, 0) - mean) / word_to_sd[word]
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
