from general_utils import UNCONTESTED_PAUL_BOOKS, CONTESTED_PAUL_BOOKS

def get_label_color(book_label):
  if book_label in UNCONTESTED_PAUL_BOOKS:
    return "blue"
  elif book_label in CONTESTED_PAUL_BOOKS:
    return "red"
  else:
    return "green"
