import read_nt_text_utils
import os
from general_utils import FILE_TYPE_SUFFIX
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

  if chunk_size == 1500:
    book_to_text['Paul A'] = ' '.join([book_to_text['1 Thessalonians'], book_to_text['Philemon']])
    del book_to_text['1 Thessalonians']
    del book_to_text['Philemon']

    book_to_text['Ignatius A'] = ' '.join([book_to_text['Ignatius Polycarp'], book_to_text['Ignatius Smyrnaeans']])
    del book_to_text['Ignatius Polycarp']
    del book_to_text['Ignatius Smyrnaeans']

    book_to_text['Ignatius B'] = ' '.join([book_to_text['Ignatius Magnesians'], book_to_text['Ignatius Trallians']])
    del book_to_text['Ignatius Magnesians']
    del book_to_text['Ignatius Trallians']

    book_to_text['Ignatius C'] = ' '.join([book_to_text['Ignatius Philadelphians'], book_to_text['Ignatius Romans']])
    del book_to_text['Ignatius Philadelphians']
    del book_to_text['Ignatius Romans']

  elif chunk_size == 2000:
    book_to_text['Paul A'] = ' '.join([book_to_text['1 Thessalonians'], book_to_text['Philippians'], book_to_text['Philemon']])
    del book_to_text['1 Thessalonians']
    del book_to_text['Philemon']
    del book_to_text['Philippians']

    book_to_text['Ignatius A'] = ' '.join([book_to_text['Ignatius Ephesians'], book_to_text['Ignatius Polycarp']])
    del book_to_text['Ignatius Polycarp']
    del book_to_text['Ignatius Ephesians']

    book_to_text['Ignatius B'] = ' '.join([book_to_text['Ignatius Smyrnaeans'], book_to_text['Ignatius Philadelphians']])
    del book_to_text['Ignatius Smyrnaeans']
    del book_to_text['Ignatius Philadelphians']

    book_to_text['Ignatius C'] = ' '.join([book_to_text['Ignatius Magnesians'], book_to_text['Ignatius Romans'], book_to_text['Ignatius Trallians']])
    del book_to_text['Ignatius Magnesians']
    del book_to_text['Ignatius Romans']
    del book_to_text['Ignatius Trallians']

  elif chunk_size == 3000:
    book_to_text['Paul A'] = ' '.join([book_to_text['1 Thessalonians'], book_to_text['Philippians'], book_to_text['Philemon']])
    del book_to_text['1 Thessalonians']
    del book_to_text['Philemon']
    del book_to_text['Philippians']

    book_to_text['Ignatius A'] = ' '.join([book_to_text['Ignatius Ephesians'], book_to_text['Ignatius Magnesians'], book_to_text['Ignatius Philadelphians']])
    del book_to_text['Ignatius Magnesians']
    del book_to_text['Ignatius Ephesians']
    del book_to_text['Ignatius Philadelphians']

    book_to_text['Ignatius B'] = ' '.join([book_to_text['Ignatius Smyrnaeans'], book_to_text['Ignatius Polycarp'], book_to_text['Ignatius Romans'], book_to_text['Ignatius Trallians']])
    del book_to_text['Ignatius Smyrnaeans']
    del book_to_text['Ignatius Polycarp']
    del book_to_text['Ignatius Romans']
    del book_to_text['Ignatius Trallians']

  else:
    raise ValueError

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