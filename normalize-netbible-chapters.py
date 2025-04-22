import os
import unicodedata

directory = 'netbible_chapters'

# https://stackoverflow.com/a/518232
def strip_accents(s):
  return ''.join(c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn')

def normalize(text):
  result = strip_accents(text).lower().replace('|', '').replace('.', '').replace('·', '').replace('[', '').replace(']', '').replace(',', '').replace('᾿', '').replace(';', '').replace('-', '').replace('\n', '').replace('(', '').replace(')', '').replace('_', '').replace('῾', '').replace(':', '')

  without_verse_numbers = ''.join([i for i in result if not i.isdigit()])
  result = ' '.join(without_verse_numbers.split())

  # check all resulting characters to make sure they're simple greek letters
  for c in result:
    if ord(c) not in range(945, 970) and c != ' ':
      print('ERROR:' + c)

  return result

for filename in os.listdir(directory):
  if '-norm' not in filename:
    with open(os.path.join(directory, filename), 'r') as handle:
      new_file_contents = ''
      for line in handle:
        new_file_contents += normalize(line)

      with open(os.path.join(directory, filename[:-4] + "-norm.txt"), 'w') as file:
        file.write(new_file_contents)
