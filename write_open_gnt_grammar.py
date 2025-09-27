import pandas as pd
import os
from general_utils import BOOK_NAMES

data = pd.read_csv("OpenGNT_keyedFeatures.csv", sep = '\t')

# "Book number, ranging from 40 to 66, representing books from Matthew to the book of Revelation."
books = [int(val.split('｜')[0][1:]) for val in data['〔book｜chapter｜verse〕']]
chapters = [int(val.split('｜')[1]) for val in data['〔book｜chapter｜verse〕']]
verses = [int(val.split('｜')[2][:-1]) for val in data['〔book｜chapter｜verse〕']]

def tantt_to_part_of_speech(tantt_cell):
  primary_tantt_info = tantt_cell.split(';')[0]
  tags = primary_tantt_info.split('=')
  if len(tags) > 3:
    return tags[3]
  return '' # No word here, so no part of speech label

# "Corresponding TANTT data aligned with OGNT"
# TODO make sure no spaces in here
parts_of_speech = [tantt_to_part_of_speech(cell) for cell in data['〔TANTT〕']]
if any(' ' in part for part in parts_of_speech):
  raise ValueError("error: space character present in part of speech tag")

book_to_parts_of_speech = {}

for book_index, chapter, verse, part in zip(books, chapters, verses, parts_of_speech):
  book = BOOK_NAMES[book_index - 40]
  if book not in book_to_parts_of_speech:
    book_to_parts_of_speech[book] = ''

  if book == 'john':
    if chapter == 7 and verse == 53:
      continue
    elif chapter == 8 and verse < 12:
      continue
  elif book == 'mark' and chapter == 16 and verse > 8:
    continue

  book_to_parts_of_speech[book] += part + ' '

for book, parts_of_speech in book_to_parts_of_speech.items():
  with open(os.path.join('opengnt_grammar', book + ".txt"), 'w') as file:
    file.write(parts_of_speech)
