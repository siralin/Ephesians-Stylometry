import re
from read_nt_text_utils import read_non_normalized_texts

def _get_sentence_lengths(text):
  return [sen.count(' ') + 1 for sen in re.split(r'[\.\;]', text)]

# Returns a dict of each book name to a list of the length of each sentence in the book, in order.
def read_sentence_lengths():
  book_to_text = read_non_normalized_texts()
  return {book: _get_sentence_lengths(text) for book, text in book_to_text.items()}
