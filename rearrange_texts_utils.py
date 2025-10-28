
def find_nth_space(text: str, n: int) -> int:
    index = text.find(' ')
    while index >= 0 and n > 1:
        index = text.find(' ', index + 1)
        n -= 1
    return index

def merge_colossians_ephesians_texts(book_to_text):
  book_to_text['ColEph'] = book_to_text['Colossians'] + ' ' + book_to_text['Ephesians']
  del book_to_text['Colossians']
  del book_to_text['Ephesians']

def merge_ignatian_texts(book_to_text):
  all_ignatius = []
  for book in set(book_to_text.keys()):
    if 'Ignatius' in book:
      all_ignatius.append(book_to_text[book])
      del book_to_text[book]

  book_to_text['Ignatius'] = ' '.join(all_ignatius)

def merge_pauline_texts(book_to_text):
  all_paul = ' '.join(book_to_text['Romans'] + book_to_text['1 Corinthians'] + book_to_text['2 Corinthians'] + book_to_text['Galatians'] + book_to_text['Philippians'] + book_to_text['1 Thessalonians'] + book_to_text['Philemon'])

  book_to_text['Paul'] = all_paul

  del book_to_text['Romans']
  del book_to_text['1 Corinthians']
  del book_to_text['2 Corinthians']
  del book_to_text['Galatians']
  del book_to_text['Philippians']
  del book_to_text['1 Thessalonians']
  del book_to_text['Philemon']

# Reorganize Pauline texts to be about 4000 words long
def rearrange_pauline_texts(book_to_text):
  romans = book_to_text['Romans']
  romans_split_index = find_nth_space(romans, 4000)
  paul_a = romans[:romans_split_index]

  one_corinthians = book_to_text['1 Corinthians']
  one_cor_split_index = find_nth_space(one_corinthians, 889)
  one_cor_split_index_2 = find_nth_space(one_corinthians, 4889)
  paul_b = romans[romans_split_index + 1:] + ' '+ one_corinthians[:one_cor_split_index]
  paul_c = one_corinthians[one_cor_split_index + 1:one_cor_split_index_2]

  two_corinthians = book_to_text['2 Corinthians']
  two_cor_split_index = find_nth_space(two_corinthians, 2059)
  paul_d = one_corinthians[one_cor_split_index_2 + 1:] + ' ' + two_corinthians[:two_cor_split_index]

  galatians = book_to_text['Galatians']
  gal_split_index = find_nth_space(galatians, 1582)
  paul_e = two_corinthians[two_cor_split_index + 1:] + ' ' + galatians[:gal_split_index]
  paul_f = ' '.join([galatians[gal_split_index + 1:] + book_to_text['Philippians'] + book_to_text['1 Thessalonians'] + book_to_text['Philemon']])

  for book in [paul_a, paul_b, paul_c, paul_d, paul_e, paul_f]:
    print(len(book.split(' ')))

  book_to_text['Paul A'] = paul_a
  book_to_text['Paul B'] = paul_b
  book_to_text['Paul C'] = paul_c
  book_to_text['Paul D'] = paul_d
  book_to_text['Paul E'] = paul_e
  book_to_text['Paul R'] = paul_f

  del book_to_text['Romans']
  del book_to_text['1 Corinthians']
  del book_to_text['2 Corinthians']
  del book_to_text['Galatians']
  del book_to_text['Philippians']
  del book_to_text['1 Thessalonians']
  del book_to_text['Philemon']
