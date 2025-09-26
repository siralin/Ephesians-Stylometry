import unittest
from ngram_utils import _normalize_frequencies_to_zscore
from statistics import stdev, fmean

class TestNormalizeFrequenciesToZscore(unittest.TestCase):

  # Tests that the frequencies are adjusted so the mean is 0 and the std dev is 1,
  # when there's only one ngram we're looking at.
  def test_normalize_frequencies_to_zscore_single_ngram(self):
    title_to_ngram_frequencies = [
      [2/40], [4/400], [4/480], [4/10], [5/20], [5/60], [7/40], [9/40]]

    title_to_ngram_zscores = _normalize_frequencies_to_zscore(title_to_ngram_frequencies)

    self.assertEqual(len(title_to_ngram_zscores), 8)
    for zscores in title_to_ngram_zscores:
      self.assertEqual(len(zscores), 1)

    zscores = [z[0] for z in title_to_ngram_zscores]
    self.assertAlmostEqual(fmean(zscores), 0)
    self.assertAlmostEqual(stdev(zscores), 1)

  # Tests that the frequencies are independently adjusted so the mean is 0 and the std dev is 1,
  # when we're looking at multiple ngrams at once.
  def test_normalize_frequencies_to_zscore_multiple_ngram(self):
    title_to_ngram_frequencies = [ [0.1, 0.05], [0.1, 0.04], [0.08, 0], [0, 0.1] ]

    title_to_ngram_zscores = _normalize_frequencies_to_zscore(title_to_ngram_frequencies)

    self.assertEqual(len(title_to_ngram_zscores), 4)
    for zscores in title_to_ngram_zscores:
      self.assertEqual(len(zscores), 2)

    for i in range(2):
      zscores = [z[i] for z in title_to_ngram_zscores]
      self.assertAlmostEqual(fmean(zscores), 0)
      self.assertAlmostEqual(stdev(zscores), 1)

if __name__ == '__main__':
    unittest.main()