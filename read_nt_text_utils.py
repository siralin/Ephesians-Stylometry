import os
from general_utils import FILE_TYPE_SUFFIX, NORMALIZED_FILE_SUFFIX, TEXT_DIRECTORY, GRAMMAR_DIRECTORY
from chunk_text_utils import break_into_chunks

# Returns dictionary of book name to all text in the book, including sentence-ending punctuation
# and accents.  Includes a space between each pair of words.
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

# Does NOT include books that are too short (except the merged Paul A)
def read_parts_of_speech_in_chunks(ideal_chunk_size, min_chunk_size):
  book_to_parts = read_parts_of_speech()

  # These are not epistles, so we don't want them.
  del book_to_parts['Matthew']
  del book_to_parts['Mark']
  del book_to_parts['Luke']
  del book_to_parts['John']
  del book_to_parts['Acts']

  if ideal_chunk_size == 1500:
    book_to_parts['Paul A'] = ' '.join([book_to_parts['1 Thessalonians'], book_to_parts['Philemon']])
    del book_to_parts['1 Thessalonians']
    del book_to_parts['Philemon']

  elif ideal_chunk_size >= 2000 and ideal_chunk_size <= 3000:
    book_to_parts['Paul A'] = ' '.join([book_to_parts['1 Thessalonians'], book_to_parts['Philippians'], book_to_parts['Philemon']])
    del book_to_parts['1 Thessalonians']
    del book_to_parts['Philemon']
    del book_to_parts['Philippians']
  else:
    raise ValueError('define actions for chunk size ' + str(ideal_chunk_size))

  book_to_chunks = break_into_chunks(book_to_parts, ideal_chunk_size)

  for book, chunk in list(book_to_chunks.items()):
    if len(chunk.split()) < min_chunk_size and book not in ['Ephesians', 'Colossians']:
      del book_to_chunks[book]

  return book_to_chunks
