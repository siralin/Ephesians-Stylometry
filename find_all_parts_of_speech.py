from read_nt_text_utils import read_parts_of_speech

book_to_parts = read_parts_of_speech()

unique_parts = set()
for text_parts in book_to_parts.values():
  unique_parts.update(text_parts.split())

for part in sorted(unique_parts):
  print(part) # TODO a few mysterious broken/special characters