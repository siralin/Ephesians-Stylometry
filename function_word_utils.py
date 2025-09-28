from collections import Counter
from statistics import stdev, fmean
from unit_frequency_utils import unit_counts_to_normalized_frequencies_for_given_units

# The top 100 most common words in the NT, with nouns and non-"to be" verbs removed.
FUNCTION_WORDS = ['ΚΑΙ', 'Ο', 'ΕΝ', 'ΔΕ', 'ΤΟΥ', 'ΕΙΣ', 'ΤΟ', 'ΤΟΝ', 'ΤΗΝ', 'ΑΥΤΟΥ', 'Η', 'ΤΗΣ', 'ΟΤΙ', 'ΤΩ', 'ΤΩΝ', 'ΟΙ', 'ΓΑΡ', 'ΜΗ', 'ΑΥΤΟΝ', 'ΕΣΤΙΝ', 'ΤΗ', 'ΑΥΤΩ', 'ΤΑ', 'ΟΥ', 'ΟΥΚ', 'ΤΟΥΣ', 'ΠΡΟΣ',
  #'ΘΕΟΥ',
  'ΕΚ', 'ΙΝΑ', 'ΕΠΙ', 'ΤΟΙΣ', 'ΥΜΙΝ',
  #'ΕΙΠΕΝ',
  'ΕΙ', 'ΑΥΤΩΝ', 'ΜΟΥ', 'ΥΜΩΝ', 'ΑΥΤΟΙΣ', 'ΔΙΑ', 'ΩΣ', 'ΟΥΝ', 'ΣΟΥ', 'ΑΠΟ',
  #'ΙΗΣΟΥΣ',
  'ΤΙ', 'ΑΛΛΑ', 'ΥΜΑΣ', 'ΗΝ', 'ΗΜΩΝ', 'ΤΙΣ', 'ΑΥΤΟΥΣ', 'ΕΓΩ', 'ΤΑΣ',
  #'ΛΕΓΕΙ',
  'ΕΑΝ', 'ΠΕΡΙ',
  #'ΙΗΣΟΥ',
  'ΚΑΤΑ', 'ΤΟΥΤΟ',
  #'ΘΕΟΣ',
  'ΜΕΤΑ', 'ΜΕ',
  #'ΠΑΝΤΑ',
  #'ΧΡΙΣΤΟΥ',
  'ΕΞ',
  #'ΚΥΡΙΟΥ',
  'ΥΜΕΙΣ', 'ΤΑΥΤΑ', 'ΜΟΙ', 'ΑΛΛ', 'ΟΣ', 'ΣΟΙ', 'ΤΕ',
  #'ΛΕΓΩ',
  'ΟΥΤΩΣ', 'ΤΑΙΣ',
  #'ΕΓΕΝΕΤΟ',
  #'ΙΔΟΥ',
  'ΣΕ', 'ΑΥΤΗ', 'ΟΥΤΟΣ', 'ΥΠΟ', 'ΚΑΘΩΣ',
  #'ΛΕΓΩΝ',
  'ΜΕΝ',
  #'ΠΑΝΤΕΣ',
  #'ΚΥΡΙΟΣ',
  'ΣΥ', 'ΑΥΤΗΣ', 'ΟΝ', 'ΗΜΙΝ', 'ΑΥΤΟΣ', 'ΑΝ', 'ΗΜΑΣ',
  #'ΥΙΟΣ',
  'ΤΟΤΕ',
  #'ΘΕΩ',
  #'ΠΝΕΥΜΑ',
  'ΕΙΣΙΝ'
  ]

# Returns a tuple of a 2d array and a list of words
# where array[book index][word index] = zscore
# and the book index matches the index of the same book in the given book_to_word_counts
# and the word index matches the index of the same word in the returned list of words.
#
# book_to_text: Dict of book title to all the text in that book, appropriately normalized.  May or may not contain whitespace.
# function_words: int, the words the frequencies should be calculated for
# normalization_method: whether to normalize frequencies by 'zscore' or 'simple' method
def calculate_normalized_function_word_frequencies(book_to_text, function_words, normalization_method):
  # first, calculate frequency of every possible word in each book.
  # This is a list of Counters, one for each word
  book_to_word_counts = [None] * len(book_to_text)
  overall_word_counts = Counter()

  for index, book in enumerate(book_to_text):
    words = book_to_text[book].split(' ')
    book_to_word_counts[index] = Counter(words)
    overall_word_counts.update(words)

  return unit_counts_to_normalized_frequencies_for_given_units(
    function_words, book_to_word_counts, overall_word_counts, normalization_method)
