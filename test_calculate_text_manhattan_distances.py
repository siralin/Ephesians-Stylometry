import unittest
from delta_utils import calculate_text_manhattan_distances

class TestCalculateTextManhattanDistances(unittest.TestCase):

  def test_calculate_text_manhattan_distances(self):
    title_to_word_zscores = {
      'textA': {'a': 0.5, 'b': 0.7, 'c': 0.2},
      'textB': {'a': 0.1, 'b': 0.7, 'c': -0.6}}
    manhattan_distances = calculate_text_manhattan_distances(title_to_word_zscores)

    # 0.4 + 0 + 0.8 = 1.2
    self.assertAlmostEqual(manhattan_distances['textA']['textB'], 1.2)
    self.assertAlmostEqual(manhattan_distances['textB']['textA'], 1.2)

    self.assertEqual(manhattan_distances['textA']['textA'], 0)
    self.assertEqual(manhattan_distances['textB']['textB'], 0)

if __name__ == '__main__':
    unittest.main()
