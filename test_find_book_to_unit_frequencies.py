import unittest
from collections import Counter
from unit_frequency_utils import _find_book_to_unit_frequencies

class TestFindBookToUnitFrequencies(unittest.TestCase):

  def test_find_book_to_unit_frequencies(self):
    book_to_unigram_counts = [
      Counter({'a': 2}),
      Counter({'a': 1, 'b': 3}),
      Counter({'c': 5})]
    most_frequent_unigrams = ['a', 'b']
    frequencies = _find_book_to_unit_frequencies(book_to_unigram_counts, most_frequent_unigrams)

    self.assertEqual(len(frequencies), 3)
    self.assertEqual(frequencies[0], [1, 0])
    self.assertEqual(frequencies[1], [0.25, 0.75])
    self.assertEqual(frequencies[2], [0, 0])

if __name__ == '__main__':
    unittest.main()
