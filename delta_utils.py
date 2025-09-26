import os
from collections import Counter
from statistics import stdev, fmean
from general_utils import UNCONTESTED_PAUL_BOOKS, CONTESTED_PAUL_BOOKS, TEXT_DIRECTORY, NORMALIZED_FILE_SUFFIX

# Teturns a dictionary of book name
#   to dictionary of chapter number to text of that chapter,
#   with the text normalized to remove all punctuation and capitalization.
# WARNING: includes 'parallel' and 'unique' book divisions for some books
def read_normalized_texts_netbible():
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

# reads in the netbible chapter texts and
# returns a dictionary of book name
#   to dictionary of word to z-score (normalized frequency)
# TODO test this
def read_and_calculate_text_to_zscores(num_most_frequent_words):
  book_to_word_counts = read_in_book_to_word_counts()
  total_word_counts = Counter()
  for _, word_counts in book_to_word_counts.items():
    total_word_counts.update(word_counts)

  return word_counts_to_zscores(num_most_frequent_words, book_to_word_counts, total_word_counts)

# Returns dictionary of book title to Counter of every word in it.
def read_in_book_to_word_counts():
  book_to_word_counts = {}

  # count all words in each book and overall
  for filename in os.listdir(TEXT_DIRECTORY):
    if NORMALIZED_FILE_SUFFIX in filename and 'unique' not in filename and 'parallel' not in filename:
      book = filename[:filename.index('-', 2)]
      if book not in book_to_word_counts:
        book_to_word_counts[book] = Counter()

      with open(os.path.join(TEXT_DIRECTORY, filename), 'r') as handle:
        for line in handle:
          words = line.split()
          for word in words:
            book_to_word_counts[book][word] += 1
  return book_to_word_counts

def find_zscores_for_given_words(words):
  book_to_word_counts = read_in_book_to_word_counts()
  book_to_word_frequencies = find_book_to_word_frequencies(book_to_word_counts, words)
  return normalize_frequencies_to_zscore(words, book_to_word_frequencies)
