import read_nt_text_utils
import os
from general_utils import FILE_TYPE_SUFFIX, NORMALIZED_FILE_SUFFIX, TEXT_DIRECTORY


# Returns dictionary of book name to all text in the book, including sentence-ending punctuation
# and accents.  Includes a space between each pair of words.
# Includes the Septuagint and various other ancient texts.
#
# TODO remove verse numbers, chapter numbers etc
def read_non_normalized_texts():
  book_to_text = read_nt_text_utils.read_non_normalized_texts()
  book_to_text.update(read_text_from_directory('septuagint'))
  book_to_text.update(read_text_from_directory('other-texts'))

  return book_to_text

# Returns dictionary of book name to all text in the book, including sentence-ending punctuation
# and accents.  Includes a space between each pair of words.
def read_text_from_directory(directory):
  book_to_text = {}

  for filename in os.listdir(directory):
    if NORMALIZED_FILE_SUFFIX not in filename:
      book = filename[: 0 - len(FILE_TYPE_SUFFIX)]

      with open(os.path.join(directory, filename), 'r') as handle:
        book_to_text[book] = handle.read()

  print(book_to_text.keys())
  return book_to_text
