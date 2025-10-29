import unittest
from rearrange_texts_utils import merge_pauline_texts

class TestRearrangeTextsUtils(unittest.TestCase):

  def test_merge_pauline_texts(self):
    book_to_text = {}
    book_to_text['Romans'] = 'Alpha'
    book_to_text['1 Corinthians'] = 'Beta'
    book_to_text['2 Corinthians'] = 'Gamma'
    book_to_text['Galatians'] = 'Delta'
    book_to_text['Philippians'] = 'Epsilon'
    book_to_text['1 Thessalonians'] = 'Zeta'
    book_to_text['Philemon'] = 'Eta'

    merge_pauline_texts(book_to_text)
    self.assertEqual(len(book_to_text), 1)
    self.assertEqual(book_to_text['Paul'], 'Alpha Beta Gamma Delta Epsilon Zeta Eta')

if __name__ == '__main__':
    unittest.main()
