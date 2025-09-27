import unittest
from read_text_utils import read_normalized_texts

class TestReadNormalizedTexts(unittest.TestCase):

  def test_read_normalized_texts(self):
    book_to_text = read_normalized_texts()
    self.assertEqual(len(book_to_text), 27)
    self.assertTrue(book_to_text['matthew'].startswith('ΒΙΒΛΟΣ ΓΕΝΕΣΕΩΣ ΙΗΣΟΥ ΧΡΙΣΤΟΥ'))

if __name__ == '__main__':
    unittest.main()
