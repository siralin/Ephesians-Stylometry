import unittest
from delta_utils import read_normalized_texts

class TestReadNormalizedTexts(unittest.TestCase):

  def test_read_normalized_texts(self):
    book_to_chapter_num_to_text = read_normalized_texts()
    self.assertEqual(len(book_to_chapter_num_to_text), 27 + 2*2) # books plus parallel/unique splits
    self.assertEqual(len(book_to_chapter_num_to_text['matthew']), 28)
    self.assertTrue(book_to_chapter_num_to_text['matthew'][1].startswith('βιβλος γενεσεως ιησου χριστου'))

if __name__ == '__main__':
    unittest.main()
