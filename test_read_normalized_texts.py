import unittest
from read_nt_text_utils import read_normalized_texts

class TestReadNormalizedTexts(unittest.TestCase):

  def test_read_normalized_texts(self):
    book_to_text = read_normalized_texts()
    self.assertEqual(len(book_to_text), 27)
    self.assertEqual(book_to_text['Matthew'][:29], 'βιβλος γενεσεως ιησου χριστου')

if __name__ == '__main__':
    unittest.main()
