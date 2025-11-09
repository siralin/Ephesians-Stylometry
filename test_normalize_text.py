import unittest
from text_normalization_utils import normalize

class TestNormalizeText(unittest.TestCase):

  def test_normalize(self):
    text = 'Συ δε λαλει α πρεπει τη υγιαινουση διδασκαλια.'
    norm = normalize(text)
    self.assertEqual('συ δε λαλει α πρεπει τη υγιαινουση διδασκαλια', norm)

if __name__ == '__main__':
    unittest.main()
