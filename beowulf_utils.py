from delta_utils import read_normalized_texts
from nltk.util import ngrams
from collections import Counter
import general_utils

def read_book_texts():
  book_to_chapter_to_text = read_normalized_texts()

  # then get rid of parallel/unique texts
  del book_to_chapter_to_text['ephesiansparallel']
  del book_to_chapter_to_text['colossiansparallel']
  del book_to_chapter_to_text['ephesiansunique']
  del book_to_chapter_to_text['colossiansunique']

  # (Note that if you don't delete either the originals or the parallel/unique texts,
  # you get incorrect information about the most common words/bigrams/etc)

  books = {}
  for book, chapter_to_text in book_to_chapter_to_text.items():
    book_text = ''
    for c in range(0, len(chapter_to_text)):
      book_text += chapter_to_text[c+1]
    books[book] = ''.join(book_text.split()) # or book_text to keep spaces in
  return books

def find_interesting_bigrams(all_text, num_ngrams_wanted, ngram_size):
  # Take the most common bigrams that don't include spaces.
  all_bigrams = ngrams(all_text, ngram_size) # includes spaces
  letter_bigrams = [bi for bi in all_bigrams if " " not in bi]
  bigram_counts = Counter(letter_bigrams)
  return bigram_counts.most_common(num_ngrams_wanted)

# Convert counts to frequencies.
#   (Within each book, the number of ngram occurrences
#    divided by the number of non-space characters.)
def calculate_ngram_frequencies(interesting_bigrams, books):
  bigram_to_book_to_frequency = [[0 for x in range(len(books))] for y in range(len(interesting_bigrams))]

  for book_index, book in enumerate(books):
    book_text = books[book]
    text_length = len(book_text) - book_text.count(' ')
    for bigram_index, bigram in enumerate(interesting_bigrams):
      bigram_count = book_text.count("".join(bigram[0]))
      bigram_to_book_to_frequency[bigram_index][book_index] = bigram_count / text_length
  return bigram_to_book_to_frequency

# Normalize frequencies _per ngram_ (cross-book) to between -1, 1
def normalize_ngram_frequencies(bigram_to_book_to_frequency):
  num_ngrams = len(bigram_to_book_to_frequency)
  bigram_to_book_to_norm_freq = [[]] * num_ngrams

  for bigram_index in range(num_ngrams):
    max_freq = max(bigram_to_book_to_frequency[bigram_index])
    min_freq = min(bigram_to_book_to_frequency[bigram_index])
    multiplier = 2 / (max_freq - min_freq)
    bigram_to_book_to_norm_freq[bigram_index] = [(x - min_freq) * multiplier - 1 for x in bigram_to_book_to_frequency[bigram_index]]
  return bigram_to_book_to_norm_freq
