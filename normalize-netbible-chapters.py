import os
import unicodedata
from general_utils import TEXT_DIRECTORY, PARALLEL_TEXT_SUBDIRECTORY, NORMALIZED_FILE_SUFFIX

# https://stackoverflow.com/a/518232
def strip_accents(s):
  return ''.join(c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn')

def normalize(text): # TODO may need to do better with text inside brackets
  result = strip_accents(text).lower().replace('|', '').replace('.', '').replace('·', '').replace('[', '').replace(']', '').replace(',', '').replace('᾿', '').replace(';', '').replace('-', '').replace('\n', '').replace('(', '').replace(')', '').replace('_', '').replace('῾', '').replace(':', '')

  without_verse_numbers = ''.join([i for i in result if not i.isdigit()])
  result = ' '.join(without_verse_numbers.split())

  # check all resulting characters to make sure they're simple greek letters
  for c in result:
    if ord(c) not in range(945, 970) and c != ' ':
      print('ERROR:' + c)

  return result

def normalize_files_in_dir(directory):
  for filename in os.listdir(directory):
    if filename == PARALLEL_TEXT_SUBDIRECTORY:
      # TODO may want to preserve these line breaks
      normalize_files_in_dir(TEXT_DIRECTORY + "/" + PARALLEL_TEXT_SUBDIRECTORY)
    elif NORMALIZED_FILE_SUFFIX not in filename:
      with open(os.path.join(directory, filename), 'r') as handle:
        new_file_contents = ''
        for line in handle:
          new_file_contents += normalize(line)

        with open(os.path.join(directory, filename[:-4] + NORMALIZED_FILE_SUFFIX + ".txt"), 'w') as file:
          file.write(new_file_contents)

normalize_files_in_dir(TEXT_DIRECTORY)