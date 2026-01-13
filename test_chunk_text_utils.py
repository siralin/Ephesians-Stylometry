import unittest
from chunk_text_utils import _break_up

class TestChunkTextUtils(unittest.TestCase):

  # No need to break anything or add a letter to the label if it's already short enough
  def test_dont_break_up(self):
    book_to_text = _break_up('2 Title', 'this is short', 2)
    self.assertEqual(len(book_to_text), 1)
    self.assertEqual(list(book_to_text.keys()), ['2 Title'])
    self.assertEqual(book_to_text['2 Title'], 'this is short')

  # No need to break anything or add a letter to the label if it's already too short
  def test_dont_break_up_very_short(self):
    book_to_text = _break_up('3 Title', 'this is too short', 5)
    self.assertEqual(len(book_to_text), 1)
    self.assertEqual(list(book_to_text.keys()), ['3 Title'])
    self.assertEqual(book_to_text['3 Title'], 'this is too short')

  def test_break_up(self):
    book_to_text = _break_up('Title', 'this is a sentence of precisely nine words really', 4)
    self.assertEqual(len(book_to_text), 2)
    self.assertEqual(list(book_to_text.keys()), ['Title A', 'Title B'])
    self.assertEqual(book_to_text['Title A'], 'this is a sentence')
    self.assertEqual(book_to_text['Title B'], 'of precisely nine words really')

if __name__ == '__main__':
    unittest.main()
