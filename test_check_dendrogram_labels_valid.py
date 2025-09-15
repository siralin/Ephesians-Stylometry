import unittest
from delta_plot_utils import check_dendrogram_labels_valid

class TestCheckDendrogramLabelsValid(unittest.TestCase):

  def test_check_labels_valid_left(self):
    self.assertTrue(check_dendrogram_labels_valid(['blue', 'blue', 'blue', 'blue', 'blue', 'blue', 'blue', 'red', 'green']))

  def test_check_labels_valid_right(self):
    self.assertTrue(check_dendrogram_labels_valid(['red', 'green', 'blue', 'blue', 'blue', 'blue', 'blue', 'blue', 'blue']))

  def test_check_labels_valid_middle(self):
    self.assertTrue(check_dendrogram_labels_valid(['red', 'blue', 'blue', 'blue', 'blue', 'blue', 'blue', 'blue', 'green']))

  def test_check_invalid_split(self):
    self.assertFalse(check_dendrogram_labels_valid(['blue', 'blue', 'blue', 'green', 'blue', 'blue', 'blue', 'blue', 'green']))

  def test_check_valid_split(self):
    self.assertTrue(check_dendrogram_labels_valid(['blue', 'blue', 'blue', 'red', 'blue', 'blue', 'blue', 'blue', 'green']))

if __name__ == '__main__':
    unittest.main()
