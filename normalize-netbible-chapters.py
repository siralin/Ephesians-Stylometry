import os
import unicodedata
from normalization_utils import normalize
from general_utils import TEXT_DIRECTORY, NORMALIZED_FILE_SUFFIX

def normalize_files_in_dir(directory):
  for filename in os.listdir(directory):
    if NORMALIZED_FILE_SUFFIX not in filename:
      with open(os.path.join(directory, filename), 'r') as handle:
        lines = [normalize(line) for line in handle]
        new_file_contents = ' '.join(lines)

        with open(os.path.join(directory, filename[:-4] + NORMALIZED_FILE_SUFFIX + ".txt"), 'w') as file:
          file.write(new_file_contents)

normalize_files_in_dir(TEXT_DIRECTORY)