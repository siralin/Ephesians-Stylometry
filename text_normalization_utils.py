import unicodedata
import os
from general_utils import FILE_TYPE_SUFFIX, NORMALIZED_FILE_SUFFIX, TEXT_DIRECTORY

# https://stackoverflow.com/a/518232
def strip_accents(s):
  return ''.join(c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn')

def normalize(text):
  result = strip_accents(text).upper()

  without_verse_numbers = ''.join([i for i in result if not i.isdigit()])
  result = ' '.join(without_verse_numbers.split())

  # check all resulting characters to make sure they're simple greek letters
  for c in result:
    if ord(c) not in range(913, 938) and c != ' ':
      print('ERROR:' + c)

  return result

# Returns dictionary of book name to all text in the book.
# Includes a space between each pair of words.
def read_normalized_texts():
  book_to_text = {}

  for filename in os.listdir(TEXT_DIRECTORY):
    if NORMALIZED_FILE_SUFFIX in filename:
      book = filename[: 0 - len(FILE_TYPE_SUFFIX) - len(NORMALIZED_FILE_SUFFIX)]

      with open(os.path.join(TEXT_DIRECTORY, filename), 'r') as handle:
        book_to_text[book] = handle.read()

  return book_to_text