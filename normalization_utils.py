import unicodedata

# https://stackoverflow.com/a/518232
def strip_accents(s):
  return ''.join(c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn')

def normalize(text):
  result = strip_accents(text).upper()

  without_verse_numbers = ''.join([i for i in result if not i.isdigit()])
  result = ' '.join(without_verse_numbers.split())

  # check all resulting characters to make sure they're simple greek letters
  for c in result:
    if ord(c) not in range(913, 938) and c != ' ':
      print('ERROR:' + c)

  return result