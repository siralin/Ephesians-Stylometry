import os

UNCONTESTED_PAUL_BOOKS = ["Romans", "1 Corinthians", "2 Corinthians", "Galatians", "Philippians", "1 Thessalonians", "Philemon"]

# TODO rename category
CONTESTED_PAUL_BOOKS = ["Ephesians", "Colossians"]

DISPUTED_PAUL_BOOKS = ['2 Thessalonians', '1 Timothy', '2 Timothy', 'Titus']

TEXT_DIRECTORY = 'opengnt_books'
GRAMMAR_DIRECTORY = 'opengnt_grammar' # opengnt_grammar or opengnt_simple_grammar
NORMALIZED_FILE_SUFFIX = '-norm'
FILE_TYPE_SUFFIX = '.txt'

BOOK_NAMES = ['Matthew', 'Mark', 'Luke', 'John', 'Acts', 'Romans', '1 Corinthians', '2 Corinthians', 'Galatians', 'Ephesians', 'Philippians', 'Colossians', '1 Thessalonians', '2 Thessalonians', '1 Timothy', '2 Timothy', 'Titus', 'Philemon', 'Hebrews', 'James', '1 Peter', '2 Peter', '1 John', '2 John', '3 John', 'Jude', 'Revelation']

def find_septuagint_books():
  books = []
  for filename in os.listdir('septuagint'):
    book = filename[: 0 - len(FILE_TYPE_SUFFIX)]
    books.append(book)
  return books

SEPTUAGINT_BOOKS = find_septuagint_books()
