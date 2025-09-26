import unittest
from text_normalization_utils import normalize

class TestReadNormalizedTexts(unittest.TestCase):

  def test_normalize(self):
    text = 'Συ δε λαλει α πρεπει τη υγιαινουση διδασκαλια.'
    norm = normalize(text)
    self.assertEqual('ΣΥ ΔΕ ΛΑΛΕΙ Α ΠΡΕΠΕΙ ΤΗ ΥΓΙΑΙΝΟΥΣΗ ΔΙΔΑΣΚΑΛΙΑ', norm)

if __name__ == '__main__':
    unittest.main()
