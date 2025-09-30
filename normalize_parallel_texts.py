import os
from general_utils import FILE_TYPE_SUFFIX, NORMALIZED_FILE_SUFFIX

for filename in os.listdir('netbible_parallels'):
  print(filename)
  text = ''
  if NORMALIZED_FILE_SUFFIX in filename:
    with open(os.path.join('netbible_parallels', filename), 'r') as handle:
      text = handle.read()

    text = text.upper()
    with open(os.path.join('netbible_parallels', filename), 'w') as handle:
      handle.write(text)
