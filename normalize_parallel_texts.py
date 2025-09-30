import os
from general_utils import FILE_TYPE_SUFFIX, NORMALIZED_FILE_SUFFIX

def normalize_parallel_texts():
  for filename in os.listdir('netbible_parallels'):
    text = ''
    if NORMALIZED_FILE_SUFFIX in filename:
      with open(os.path.join(TEXT_DIRECTORY, filename), 'r') as handle:
        text = handle.read()

    text = text.upper()
    with open(os.path.join(TEXT_DIRECTORY, filename), 'w') as handle:
      file.write(text)
