
from statistics import stdev, fmean

# convert frequency to z-score (the number of standard deviations above/below the mean)
# this means that over the whole corpus,
# the mean for each word is 0 and the standard deviation is 1
#
# words: list of all the words we're interested in
# text_to_word_frequencies: dictionary of text title -> dictionary of word to frequency within text
#   (as a proportion of all words in that text).  May include words we're not interested in.
def normalize_frequencies_to_zscore(words, text_to_word_frequencies):
  word_to_mean = {}
  word_to_sd = {}
  for word in words:
    frequencies = [f[word] for f in text_to_word_frequencies.values()]
    word_to_mean[word] = fmean(frequencies)
    word_to_sd[word] = stdev(frequencies)

  book_to_word_zscores = {}
  for book, frequencies in text_to_word_frequencies.items():
    book_to_word_zscores[book] = {}
    for word, mean in word_to_mean.items():
      zscore = (frequencies[word] - mean) / word_to_sd[word]
      book_to_word_zscores[book][word] = zscore

  return book_to_word_zscores

# book_to_word_zscores: dictionary of text title to dictionary of word to its z-score
# returns dictionary of text title to
#     dictionary of other text title to manhattan distance between their z-scores
def calculate_text_manhattan_distances(book_to_word_zscores):
  manhattan_distances = {}
  for book, word_to_zscore in book_to_word_zscores.items():
    manhattan_distances[book] = {}
    for other_book, other_word_to_zscore in book_to_word_zscores.items():
      sum = 0.0
      for word, zscore in word_to_zscore.items():
        sum += abs(zscore - other_word_to_zscore[word])
      manhattan_distances[book][other_book] = sum
  return manhattan_distances
