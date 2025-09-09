import unittest
from delta_utils import find_book_to_word_frequencies

class TestFindBookToWordFrequencies(unittest.TestCase):

  def test_find_book_to_word_frequencies(self):
    book_to_word_counts = {
      'textA': {'a': 2},
      'textB': {'a': 1, 'b': 3},
      'textC': {'a': 0, 'c': 5}}
    most_frequent_words = ['a', 'b']
    frequencies = find_book_to_word_frequencies(book_to_word_counts, most_frequent_words)

    self.assertEqual(len(frequencies), 3)
    self.assertEqual(frequencies['textA'], {'a': 1, 'b': 0})
    self.assertEqual(frequencies['textB'], {'a': 0.25, 'b': 0.75})
    self.assertEqual(frequencies['textC'], {'a': 0, 'b': 0})

if __name__ == '__main__':
    unittest.main()
