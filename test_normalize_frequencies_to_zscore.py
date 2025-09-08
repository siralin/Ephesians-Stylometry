import unittest
from delta_utils import normalize_frequencies_to_zscore
from statistics import stdev, fmean

class TestNormalizeFrequenciesToZscore(unittest.TestCase):

  # Tests that the frequencies are adjusted so the mean is 0 and the std dev is 1,
  # when there's only one word we're looking at.
  def test_normalize_frequencies_to_zscore_single_word(self):
    words = ['a']
    title_to_word_frequencies = {
      'textA': {'a': 2/40},
      'textB': {'a': 4/400},
      'textC': {'a': 4/480},
      'textD': {'a': 4/10},
      'textE': {'a': 5/20},
      'textF': {'a': 5/60},
      'textG': {'a': 7/40},
      'textH': {'a': 9/40}}

    title_to_word_zscores = normalize_frequencies_to_zscore(words, title_to_word_frequencies)

    self.assertEqual(len(title_to_word_zscores), 8)
    for zscores in title_to_word_zscores.values():
      self.assertEqual(len(zscores), 1)

    zscores = [z['a'] for z in title_to_word_zscores.values()]
    self.assertAlmostEqual(fmean(zscores), 0)
    self.assertAlmostEqual(stdev(zscores), 1)

  # Tests that the frequencies are independently adjusted so the mean is 0 and the std dev is 1,
  # when we're looking at multiple words at once.
  def test_normalize_frequencies_to_zscore_multiple_word(self):
    words = ['a', 'b']
    title_to_word_frequencies = {
      'textA': {'a': 0.1, 'b': 0.05},
      'textB': {'a': 0.1, 'b': 0.04},
      'textC': {'a': 0.08},
      'textD': {'b': 0.1}}

    title_to_word_zscores = normalize_frequencies_to_zscore(words, title_to_word_frequencies)

    self.assertEqual(len(title_to_word_zscores), 4)
    for zscores in title_to_word_zscores.values():
      self.assertEqual(len(zscores), 2)

    for word in words:
      zscores = [z[word] for z in title_to_word_zscores.values()]
      self.assertAlmostEqual(fmean(zscores), 0)
      self.assertAlmostEqual(stdev(zscores), 1)

  # Tests that the frequencies are independently adjusted so the mean is 0 and the std dev is 1,
  # even when there's data in title_to_word_frequencies we don't care about
  def test_normalize_frequencies_to_zscore_ignore_other_data(self):
    words = ['a']
    title_to_word_frequencies = {
      'textA': {'a': 0.1, 'b': 0.05},
      'textB': {'a': 0.1, 'b': 0.04},
      'textC': {'a': 0.08},
      'textD': {'b': 0.1}}

    title_to_word_zscores = normalize_frequencies_to_zscore(words, title_to_word_frequencies)

    self.assertEqual(len(title_to_word_zscores), 4)
    for zscores in title_to_word_zscores.values():
      self.assertEqual(len(zscores), 1)

    zscores = [z['a'] for z in title_to_word_zscores.values()]
    self.assertAlmostEqual(fmean(zscores), 0)
    self.assertAlmostEqual(stdev(zscores), 1)


if __name__ == '__main__':
    unittest.main()