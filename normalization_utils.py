import unicodedata

# https://stackoverflow.com/a/518232
def strip_accents(s):
  return ''.join(c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn')

def normalize(text): # TODO may need to do better with text inside brackets
  result = strip_accents(text).lower().replace('|', '').replace('.', '').replace('·', '').replace('[', '').replace(']', '').replace(',', '').replace('᾿', '').replace(';', '').replace('-', '').replace('\n', ' ').replace('(', '').replace(')', '').replace('_', '').replace('῾', '').replace(':', '').replace('’', '').replace('–', '')

  without_verse_numbers = ''.join([i for i in result if not i.isdigit()])
  result = ' '.join(without_verse_numbers.split())

  # check all resulting characters to make sure they're simple greek letters
  for c in result:
    if ord(c) not in range(945, 970) and c != ' ':
      print('ERROR:' + c)

  return result