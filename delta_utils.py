import os
from collections import Counter
from statistics import stdev, fmean
from general_utils import UNCONTESTED_PAUL_BOOKS, CONTESTED_PAUL_BOOKS, TEXT_DIRECTORY, NORMALIZED_FILE_SUFFIX

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

  title_to_word_zscores = {}
  for book, frequencies in title_to_word_frequencies.items():
    title_to_word_zscores[book] = {}
    for word, mean in word_to_mean.items():
      zscore = (frequencies.get(word, 0) - mean) / word_to_sd[word]
      title_to_word_zscores[book][word] = zscore

  return title_to_word_zscores

# title_to_word_zscores: dictionary of text title to dictionary of word to its z-score
# returns dictionary of text title to
#     dictionary of other text title to manhattan distance between their z-scores
def calculate_text_manhattan_distances(title_to_word_zscores):
  manhattan_distances = {}
  for title, word_to_zscore in title_to_word_zscores.items():
    manhattan_distances[title] = {}
    for other_title, other_word_to_zscore in title_to_word_zscores.items():
      sum = 0.0
      for word, zscore in word_to_zscore.items():
        sum += abs(zscore - other_word_to_zscore[word])
      manhattan_distances[title][other_title] = sum
  return manhattan_distances

# Returns the frequencies of the given words
# (as a fraction of the total words in the book).
def find_book_to_word_frequencies(book_to_word_counts, most_frequent_words):
  book_to_frequent_word_counts = {}
  for book in book_to_word_counts.keys():
    book_to_frequent_word_counts[book] = {}
    for word in most_frequent_words:
      book_to_frequent_word_counts[book][word] = book_to_word_counts[book].get(word, 0)

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

# Teturns a dictionary of book name
#   to dictionary of chapter number to text of that chapter,
#   with the text normalized to remove all punctuation and capitalization.
def read_normalized_texts():
  book_to_chapter_to_text = {}

  for filename in os.listdir(TEXT_DIRECTORY):
    if NORMALIZED_FILE_SUFFIX in filename:
      book_chapter_hyphen_index = filename.index('-', 2)
      book = filename[:book_chapter_hyphen_index]
      post_chapter_hyphen_index = filename.index('-', book_chapter_hyphen_index + 1)
      chapter = filename[book_chapter_hyphen_index + 1:post_chapter_hyphen_index]

      if book not in book_to_chapter_to_text:
        book_to_chapter_to_text[book] = {}

      chapter_contents = ''
      with open(os.path.join(TEXT_DIRECTORY, filename), 'r') as handle:
        for line in handle:
          chapter_contents += line
      book_to_chapter_to_text[book][int(chapter)] = chapter_contents

  return book_to_chapter_to_text

def read_normalized_parallel_texts():


# reads in the netbible chapter texts and
# returns a dictionary of book name
#   to dictionary of word to z-score (normalized frequency)
# TODO test this
def read_and_calculate_text_to_zscores(num_most_frequent_words):
  book_to_word_counts = {}
  total_word_counts = Counter()

  # count all words in each book and overall
  for filename in os.listdir(TEXT_DIRECTORY):
    if NORMALIZED_FILE_SUFFIX in filename:
      book = filename[:filename.index('-', 2)]
      if book not in book_to_word_counts:
        book_to_word_counts[book] = Counter()

      with open(os.path.join(TEXT_DIRECTORY, filename), 'r') as handle:
        for line in handle:
          words = line.split()
          for word in words:
            book_to_word_counts[book][word] += 1
            total_word_counts[word] += 1
  return word_counts_to_zscores(num_most_frequent_words, book_to_word_counts, total_word_counts)

# using the given word count dicts,
# returns a dictionary of book name
#   to dictionary of word to z-score (normalized frequency)
# TODO test this
def word_counts_to_zscores(num_most_frequent_words, book_to_word_counts, total_word_counts):
  # we have a list of words
  most_frequent_words = [x[0] for x in total_word_counts.most_common(num_most_frequent_words)]

  # we have a dictionary of dictionaries
  book_to_word_frequencies = find_book_to_word_frequencies(book_to_word_counts, most_frequent_words)

  # we have a dictionary of dictionaries
  return normalize_frequencies_to_zscore(most_frequent_words, book_to_word_frequencies)
