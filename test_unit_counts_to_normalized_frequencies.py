import unittest
from collections import Counter
from unit_frequency_utils import unit_counts_to_normalized_frequencies

class TestUnitCountsToNormalizedFrequencies(unittest.TestCase):

  def test_unit_counts_to_normalized_frequencies(self):
    book_to_unit_counts = [Counter({'ab': 5, 'bc': 1}), Counter({'bc': 12, 'cd': 2}), Counter({'ab': 6, 'bc': 23})]
    overall_unit_counts = Counter({'ab': 11, 'bc': 36, 'cd': 2})
    book_to_normalized_unit_frequency, most_frequent_units = unit_counts_to_normalized_frequencies(
      2, book_to_unit_counts, overall_unit_counts, 'simple')

    self.assertEqual(len(most_frequent_units), 2)
    self.assertEqual(most_frequent_units, ['bc', 'ab'])

    #                                                     bc    ab     bc    ab      bc                    ab
    self.assertEqual(book_to_normalized_unit_frequency, [[-1.0, 1.0], [1.0, -1.0], [0.8145065398335316, -0.503448275862069]])

if __name__ == '__main__':
    unittest.main()
