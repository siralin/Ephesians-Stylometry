import unicodedata

# https://stackoverflow.com/a/518232
def strip_accents(s):
  return ''.join(c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn')

def remove_punctuation(s):
  return s.replace('.', '').replace(';', '').replace('᾽', '')

# Returns the given text with all punctuation and accents removed.
# All returned characters will be lowercase Greek letters or spaces.
def normalize(text):
  result = remove_punctuation(strip_accents(text).lower())

  # check all resulting characters to make sure they're simple greek letters
  for c in result:
    if ord(c) not in range(945, 970) and c != ' ':
      print('ERROR:' + c)

  return result
