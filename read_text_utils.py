import os
from general_utils import FILE_TYPE_SUFFIX, NORMALIZED_FILE_SUFFIX, TEXT_DIRECTORY, GRAMMAR_DIRECTORY

# Returns dictionary of book name to all non-punctuation text in the book.
# Includes a space between each pair of words.
def read_normalized_texts():
  book_to_text = {}

  for filename in os.listdir(TEXT_DIRECTORY):
    if NORMALIZED_FILE_SUFFIX in filename:
      book = filename[: 0 - len(FILE_TYPE_SUFFIX) - len(NORMALIZED_FILE_SUFFIX)]

      with open(os.path.join(TEXT_DIRECTORY, filename), 'r') as handle:
        book_to_text[book] = handle.read()

  return book_to_text

# Returns dictionary of book name to all text in the book, including certain punctuation.
# Includes a space between each pair of words.
def read_non_normalized_texts():
  book_to_text = {}

  for filename in os.listdir(TEXT_DIRECTORY):
    if NORMALIZED_FILE_SUFFIX not in filename:
      book = filename[: 0 - len(FILE_TYPE_SUFFIX)]

      with open(os.path.join(TEXT_DIRECTORY, filename), 'r') as handle:
        book_to_text[book] = handle.read()

  return book_to_text

# Returns dictionary of book name to the part of speech of every word in the book, separated by spaces.
# TODO what about removing things like 'feminine plural' as that's dependent on topic rather than author?
def read_parts_of_speech():
  book_to_text = {}

  for filename in os.listdir(GRAMMAR_DIRECTORY):
    book = filename[: 0 - len(FILE_TYPE_SUFFIX)]
    with open(os.path.join(GRAMMAR_DIRECTORY, filename), 'r') as handle:
      book_to_text[book] = handle.read()
  return book_to_text
