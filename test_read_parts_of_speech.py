import unittest
from read_nt_text_utils import read_parts_of_speech

class TestReadPartsOfSpeech(unittest.TestCase):

  def test_read_parts_of_speech_no_special_characters(self):
    book_to_text = read_parts_of_speech()
    for book, text in book_to_text.items():
      for character in text:
        if character not in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ -123':
          print('error: ' + book + ' contains special character ' + character)
          self.assertFalse(True)

if __name__ == '__main__':
    unittest.main()
