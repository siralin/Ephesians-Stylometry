from read_nt_text_utils import read_normalized_texts

book_to_text = read_normalized_texts()
for book, text in book_to_text.items():
  print(book, ',', len(text.split(' ')))