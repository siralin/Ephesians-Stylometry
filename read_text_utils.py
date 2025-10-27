import read_nt_text_utils
import os
from general_utils import FILE_TYPE_SUFFIX, NORMALIZED_FILE_SUFFIX, TEXT_DIRECTORY
from text_normalization_utils import remove_punctuation, strip_accents

# Returns dictionary of book name to all text in the book, including accents.
# Includes a space between each pair of words.  Everything is lower-case and punctuation-free.
# Includes the Septuagint and various other ancient texts.
def read_texts():
  book_to_text = read_nt_text_utils.read_non_normalized_texts()
  book_to_text.update(read_text_from_directory('septuagint'))
  book_to_text.update(read_text_from_directory('other-texts'))

  return normalize(book_to_text)

# Returns dictionary of book name to all text in the book, including sentence-ending punctuation
# and accents.  Includes a space between each pair of words.
def read_text_from_directory(directory):
  book_to_text = {}

  for filename in os.listdir(directory):
    book = filename[: 0 - len(FILE_TYPE_SUFFIX)]

    with open(os.path.join(directory, filename), 'r') as handle:
      book_to_text[book] = handle.read()

  return book_to_text

def normalize(book_to_text):
  book_to_normalized_text = {}
  for book, text in book_to_text.items():
    book_to_normalized_text[book] = remove_punctuation(text).lower()
    #for c in book_to_normalized_text[book]:
    #  # check all resulting characters to make sure they're simple greek letters
    #  if ord(strip_accents(c)) not in range(945, 970) and c != ' ':
    #    print('ERROR:' + c + ' ' + book)

  return book_to_normalized_text