import pandas as pd
import os
from general_utils import NORMALIZED_FILE_SUFFIX
from normalization_utils import normalize

data = pd.read_csv ("OpenGNT_version3_3.csv", sep = '\t')

# "Book number, ranging from 40 to 66, representing books from Matthew to the book of Revelation."
books = [int(val.split('｜')[0][1:]) for val in data['〔Book｜Chapter｜Verse〕']]

# "Greek word of OGNT in unaccented form"
words = [val.split('｜')[1] for val in data['〔OGNTk｜OGNTu｜OGNTa｜lexeme｜rmac｜sn〕']]

# Find the bits of Mark and John that should be excluded, and exclude them.
preceding_punctuation = [val.split('｜')[0][1:] for val in data['〔PMpWord｜PMfWord〕']]
following_punctuation = [val.split('｜')[1][:-1] for val in data['〔PMpWord｜PMfWord〕']]

book_names = ['matthew', 'mark', 'luke', 'john', 'acts', 'romans', '1 corinthians', '2 corinthians', 'galatians', 'ephesians', 'philippians', 'colossians', '1 thessalonians', '2 thessalonians', '1 timothy', '2 timothy', 'titus', 'philemon', 'hebrews', 'james', '1 peter', '2 peter', '1 john', '2 john', '3 john', 'jude', 'revelation']

book_to_text = {}
skip = False
for book_index, word, prec_punc, foll_punc in zip(books, words, preceding_punctuation, following_punctuation):
  book = book_names[book_index - 40]
  if book not in book_to_text:
    book_to_text[book] = ''
    if skip:
      print('error: never ended skip')
  if '[[' in prec_punc:
    if skip:
      print('error: nested [[')
    skip = True
  elif not skip:
    book_to_text[book] += word + ' '
  elif ']]' in foll_punc:
    skip = False

if skip:
  print('error: never ended skip')

for book, text in book_to_text.items():
  with open(os.path.join('opengnt_books', book + ".txt"), 'w') as file:
    file.write(text)

  with open(os.path.join('opengnt_books', book + NORMALIZED_FILE_SUFFIX + ".txt"), 'w') as file:
    file.write(normalize(text))

