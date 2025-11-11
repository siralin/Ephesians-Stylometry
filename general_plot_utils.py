from general_utils import UNCONTESTED_PAUL_BOOKS, CONTESTED_PAUL_BOOKS, DISPUTED_PAUL_BOOKS, FILE_TYPE_SUFFIX, SEPTUAGINT_BOOKS

def get_label_color(book_label):
  if book_label.startswith(tuple(UNCONTESTED_PAUL_BOOKS)) or 'Paul' in book_label:
    return "blue"
  elif book_label.startswith(tuple(CONTESTED_PAUL_BOOKS)):
    return "red"
  elif book_label.startswith(tuple(DISPUTED_PAUL_BOOKS)):
    return 'green'
  else:
    return "grey"
