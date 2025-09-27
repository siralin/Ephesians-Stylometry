import unittest
from grammar_utils import calculate_normalized_part_of_speech_ngram_frequencies

class TestGrammarUtils(unittest.TestCase):

  def test_grammar_utils(self):
    book_to_text = {'a': "ABC DEF GHI", 'b': "DEF DEF GHI"}
    book_to_ngram_frequency, ngrams = calculate_normalized_part_of_speech_ngram_frequencies(
      book_to_text, num_ngrams=1, ngram_size=1, normalization_method='simple')

    print(book_to_ngram_frequency)

if __name__ == '__main__':
    unittest.main()
