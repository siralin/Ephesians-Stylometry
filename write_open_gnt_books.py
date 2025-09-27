import pandas as pd
import os
from general_utils import NORMALIZED_FILE_SUFFIX, BOOK_NAMES
from text_normalization_utils import normalize

def _add_sentence_punctuation(following_punctuation):
  # If you add any other punctuation here, you'll have to update text_normalization_utils.normalize()

  if '.' in following_punctuation:
    return '.'
  elif ';' in following_punctuation:
    return ';'
  else:
    return ''

data = pd.read_csv("OpenGNT_version3_3.csv", sep = '\t')

# "Book number, ranging from 40 to 66, representing books from Matthew to the book of Revelation."
books = [int(val.split('｜')[0][1:]) for val in data['〔Book｜Chapter｜Verse〕']]

# "Greek word of OGNT in unaccented form"
words = [val.split('｜')[1] for val in data['〔OGNTk｜OGNTu｜OGNTa｜lexeme｜rmac｜sn〕']]

# Find punctuation so we can identify the bits of Mark and John that were definitely added later and exclude them,
# and so we can identify sentence breaks.
preceding_punctuation = [val.split('｜')[0][1:] for val in data['〔PMpWord｜PMfWord〕']]
following_punctuation = [val.split('｜')[1][:-1] for val in data['〔PMpWord｜PMfWord〕']]

book_to_text = {}
skip = False
for book_index, word, prec_punc, foll_punc in zip(books, words, preceding_punctuation, following_punctuation):
  book = BOOK_NAMES[book_index - 40]
  if book not in book_to_text:
    book_to_text[book] = ''
    if skip:
      print('error: never ended skip')
  if '[[' in prec_punc:
    if skip:
      print('error: nested [[')
    skip = True
  elif not skip:
    book_to_text[book] += word + _add_sentence_punctuation(foll_punc) + ' '
  elif ']]' in foll_punc:
    skip = False

if skip:
  print('error: never ended skip')

for book, text in book_to_text.items():
  with open(os.path.join('opengnt_books', book + ".txt"), 'w') as file:
    file.write(text)

  with open(os.path.join('opengnt_books', book + NORMALIZED_FILE_SUFFIX + ".txt"), 'w') as file:
    file.write(normalize(text))
