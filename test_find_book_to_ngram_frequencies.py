import unittest
from ngram_utils import _find_book_to_ngram_frequencies

class TestFindBookToNgramFrequencies(unittest.TestCase):

  def _find_book_to_unigram_frequencies(self):
    book_to_unigram_counts = {
      'textA': {'a': 2},
      'textB': {'a': 1, 'b': 3},
      'textC': {'a': 0, 'c': 5}}
    most_frequent_unigrams = ['a', 'b']
    frequencies = _find_book_to_ngram_frequencies(book_to_unigram_counts, most_frequent_unigrams)

    self.assertEqual(len(frequencies), 3)
    self.assertEqual(frequencies['textA'], {'a': 1, 'b': 0})
    self.assertEqual(frequencies['textB'], {'a': 0.25, 'b': 0.75})
    self.assertEqual(frequencies['textC'], {'a': 0, 'b': 0})

if __name__ == '__main__':
    unittest.main()
