import unittest
from collections import Counter
from unit_frequency_utils import unit_counts_to_normalized_frequencies

class TestUnitCountsToNormalizedFrequencies(unittest.TestCase):

  def test_unit_counts_to_normalized_frequencies(self):
    book_to_unit_counts = [Counter({'ab': 5, 'bc': 5}), Counter({'bc': 12, 'cd': 3}), Counter({'ab': 6, 'bc': 54})]
    overall_unit_counts = Counter({'ab': 11, 'bc': 71, 'cd': 9})
    book_to_normalized_unit_frequency, most_frequent_units = unit_counts_to_normalized_frequencies(
      2, book_to_unit_counts, overall_unit_counts, 'simple')

    self.assertEqual(len(most_frequent_units), 2)
    self.assertEqual(most_frequent_units, ['bc', 'ab'])

    #                                                           bc    ab     bc    ab      bc   ab
    self.assert2DListAlmostEqual(book_to_normalized_unit_frequency, [[-1.0, 1.0], [0.5, -1.0], [1.0, -0.6]])

  # https://stackoverflow.com/a/8312110
  def assert2DListAlmostEqual(self, list1, list2):
    self.assertEqual(len(list1), len(list2))
    for a, b in zip(list1, list2):
      self.assertListAlmostEqual(a, b)

  # https://stackoverflow.com/a/8312110
  def assertListAlmostEqual(self, list1, list2):
    self.assertEqual(len(list1), len(list2))
    for a, b in zip(list1, list2):
      self.assertAlmostEqual(a, b)

if __name__ == '__main__':
    unittest.main()
