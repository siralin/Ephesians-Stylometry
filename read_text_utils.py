import read_nt_text_utils
import os
from general_utils import FILE_TYPE_SUFFIX, UNCONTESTED_PAUL_BOOKS
import text_normalization_utils
from chunk_text_utils import break_into_chunks

# Returns dictionary of book name to all text in the book, not including accents.
# Includes a space between each pair of words.  Everything is lower-case and punctuation-free.
# Includes only those texts relevant to my thesis.
# Long texts are broken up (so we end up with Romans A, Romans B, Romans C, etc.)
# Certain short texts are merged.
def read_relevant_texts_in_chunks(chunk_size):
  book_to_text = read_nt_text_utils.read_non_normalized_texts()
  book_to_text.update(read_text_from_directory('other-texts'))

  # There is only one epistle in the Septuagint
  septuagint_book_to_text = read_text_from_directory('septuagint')
  book_to_text['Epistle of Jeremiah'] = septuagint_book_to_text['Epistle of Jeremiah']

  pauline_text = ' '.join([book_to_text[book] for book in UNCONTESTED_PAUL_BOOKS])
  book_to_text['Paul'] = pauline_text
  for book in UNCONTESTED_PAUL_BOOKS:
    del book_to_text[book]

  ignatius_books = [x for x in list(book_to_text.keys()) if x.startswith('Ignatius')]
  ignatius_text = ' '.join([book_to_text[book] for book in ignatius_books])
  book_to_text['Ignatius'] = ignatius_text
  for book in ignatius_books:
    del book_to_text[book]

  # The following texts are not epistles, so we don't want them.
  del book_to_text['Clement 2 Corinthians']
  del book_to_text['Didache']
  del book_to_text['Hermas Shepherd']
  del book_to_text['Matthew']
  del book_to_text['Mark']
  del book_to_text['Luke']
  del book_to_text['John']
  del book_to_text['Acts']

  return break_into_chunks(normalize(book_to_text), chunk_size)

# Returns dictionary of book name to all text in the book, not including accents.
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
    book_to_normalized_text[book] = text_normalization_utils.normalize(text).strip()

  return book_to_normalized_text