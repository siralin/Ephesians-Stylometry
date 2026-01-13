from read_text_utils import read_relevant_texts_in_chunks
from read_nt_text_utils import read_parts_of_speech_in_chunks
from word_utils import calculate_normalized_word_frequencies
from function_word_utils import calculate_normalized_function_word_frequencies
from scatter_plot_utils import generate_scatter_plot
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics.pairwise import cosine_similarity
from thesis_paul_markers import graph_paul_markers
from ngram_utils import calculate_normalized_ngram_frequencies
from grammar_utils import calculate_normalized_part_of_speech_ngram_frequencies
from dendrogram_utils import generate_dendrogram

"""
Generates figures for the thesis.

PART 1: 500 most common words
"""

IDEAL_CHUNK_SIZE = 2000
MIN_CHUNK_SIZE = 1500

NUM_WORDS_WANTED = 500
NORMALIZATION_METHOD = 'zscore'
NUM_NGRAMS_WANTED = 500
GRAMMAR_NGRAM_SIZE = 1

# for dendrograms
LINKAGE_ALGORITHM = 'average' # best at grouping Pauline books in grammar dendrogram at least
DISTANCE_METRIC = 'cosine'

book_to_text = read_relevant_texts_in_chunks(IDEAL_CHUNK_SIZE)
for book, text in book_to_text.items():
  print(book, len(text.split()))

book_names = list(book_to_text.keys())

# words: a List of the most frequent words
#
# book_to_normalized_word_frequency: a 2d List[book index][word index]
# where the book index matches the index of the same book in book_to_word_counts and book_to_text
# and the word index matches the index of the same word in words.
book_to_normalized_word_frequency, words = calculate_normalized_word_frequencies(
  book_to_text, NUM_WORDS_WANTED, NORMALIZATION_METHOD)

print(words)

xy_adjustments = {}
#generate_scatter_plot(book_to_normalized_word_frequency, book_to_text.keys(), "Figure 1", True, (0.1, -0.2), xy_adjustments, figsize=(16, 9))
plt.show()
plt.close()

"""
PART 2: remove non-function words and too-short texts
"""

for book, text in list(book_to_text.items()):
  if len(text.split()) < MIN_CHUNK_SIZE and book not in ['Ephesians', 'Colossians']:
    del book_to_text[book]

book_names = list(book_to_text.keys())

function_words = ['και', 'εν', 'του', 'ο', 'δε', 'το', 'εις', 'της', 'η', 'την', 'γαρ', 'τω', 'των', 'τον', 'αυτου', 'μη', 'οτι', 'ου', 'τα', 'εστιν', 'τη', 'ως', 'ουκ', 'ινα', 'οι', 'ημων', 'υμων', 'δια', 'εκ', 'τους', 'τοις', 'επι', 'ει', 'αλλα', 'υμας', 'αυτων', 'ουν', 'κατα', 'υμιν', 'μου', 'προς', 'απο', 'τις', 'τας', 'αυτω', 'σου', 'παντα', 'τουτο', 'αυτον', 'εαν', 'τι', 'αλλ', 'ημας', 'περι', 'δι', 'ουτως', 'υπο', 'υπερ', 'μετα', 'μεν', 'εγω', 'μοι', 'τε', 'ην', 'ημιν', 'εξ', 'ταις', 'καθως', 'ος', 'αυτοις', 'ταυτα', 'με', 'ων', 'εισιν', 'ουδε', 'ω', 'αυτους', 'αυτος', 'ειναι', 'υμεις', 'ουτε', 'νυν', 'παντες', 'παλιν', 'παντων', 'ημεις', 'σε', 'αυτης', 'ουχ', 'πως', 'επ', 'αυτη', 'μαλλον', 'α', 'αι', 'ον', 'μονον', 'σοι', 'ενωπιον', 'αν', 'οταν', 'ετι', 'παρα', 'πασιν', 'ειτε', 'ιδου', 'αυτο', 'παντας', 'συ', 'εμοι', 'παν', 'εαυτους', 'ωστε', 'ουδεν', 'κατ', 'αυτην', 'συν', 'εστε', 'εσται', 'μετ', 'ειμι', 'ωσπερ', 'διο', 'οτε', 'παντι', 'εμου', 'αυτοι', 'ης', 'πας', 'καθ', 'εφ', 'απ', 'τουτου', 'εσμεν', 'χωρις', 'μηδε', 'πασαν', 'εαυτον', 'ουτος', 'αμην', 'παση', 'τοτε', 'αλληλους', 'τινες', 'πασης', 'τινα', 'εαυτου', 'ουτοι', 'τουτω', 'επει', 'ποτε', 'εαυτοις', 'παντος', 'αυτα', 'καγω', 'ουδεις', 'αρα', 'εως', 'εκαστος', 'τουτων', 'αφ', 'παρ', 'οιτινες', 'εαυτων', 'που', 'πασα', 'πρωτον', 'προ', 'παντοτε', 'ενος', 'μηδεν', 'ηδη', 'καλως', 'οντες', 'οπως', 'ητις', 'πολλοι', 'μεθ', 'πολλα', 'οπου', 'αχρι', 'εμε', 'τουτοις', 'πολλων', 'εαυτω', 'ενα', 'ουχι', 'μητε', 'ουκετι', 'οντα', 'ενι', 'αληθως', 'οσα', 'υπ', 'γε', 'ομοιως', 'εκει', 'ταυτην', 'ουαι', 'μια', 'ητε', 'τουτον', 'νυνι', 'ειτα', 'οθεν', 'πλησιον', 'τριτον', 'μηδεις', 'ετερον', 'εμπροσθεν', 'οσοι', 'μεχρι', 'τινος', 'αρτι', 'οσον', 'μεγα', 'τινι', 'τουτ', 'σεαυτον', 'μαλιστα', 'αμα', 'ναι', 'εγγυς', 'μονος', 'καθαπερ']

# We need to renormalize because we've changed the set of texts.
book_to_normalized_word_frequency = calculate_normalized_function_word_frequencies(
  book_to_text, function_words, NORMALIZATION_METHOD)

#generate_scatter_plot(book_to_normalized_word_frequency, book_to_text.keys(), "Figure 2a", True, (0.2, -0.2))
#graph_paul_markers(book_to_text, title="Figure 3")
#generate_dendrogram(book_to_normalized_word_frequency, book_names, LINKAGE_ALGORITHM, DISTANCE_METRIC, title='Figure 2b')
#plt.show()
#plt.close()

"""
 PART X: Calculate distances using Cosine Delta
 """
distances = cosine_similarity(book_to_normalized_word_frequency)
df = pd.DataFrame(distances, index=book_names, columns=book_names)
df.to_csv('function_word_distances.csv')

"""
 PART 4: ngram analysis
 """

# ngrams: a List of the most frequent ngrams
#
# book_to_normalized_ngram_frequency: a 2d List[book index][ngram index]
# where the book index matches the index of the same book in book_to_ngram_counts and book_to_text
# and the ngram index matches the index of the same ngram in ngrams.
book_to_normalized_bigram_frequency, bigrams = calculate_normalized_ngram_frequencies(
  book_to_text, NUM_NGRAMS_WANTED, 2, NORMALIZATION_METHOD)
#generate_scatter_plot(book_to_normalized_bigram_frequency, book_to_text.keys(), "Figure 4a: Bigrams", True, (0.2, -0.2))
#generate_dendrogram(book_to_normalized_bigram_frequency, book_names, LINKAGE_ALGORITHM, DISTANCE_METRIC, 'Figure 4b')
#plt.show()
#plt.close()

bigram_distances = cosine_similarity(book_to_normalized_bigram_frequency)
bigram_df = pd.DataFrame(bigram_distances, index=book_names, columns=book_names)
bigram_df.to_csv('bigram_distances.csv')

#book_to_normalized_trigram_frequency, trigrams = calculate_normalized_ngram_frequencies(
  book_to_text, NUM_NGRAMS_WANTED, 3, NORMALIZATION_METHOD)
#generate_dendrogram(book_to_normalized_trigram_frequency, book_names, LINKAGE_ALGORITHM, DISTANCE_METRIC, 'Figure 5: Trigrams',)
#plt.show()
#plt.close()

trigram_distances = cosine_similarity(book_to_normalized_trigram_frequency)
trigram_df = pd.DataFrame(trigram_distances, index=book_names, columns=book_names)
trigram_df.to_csv('trigram_distances.csv')

"""
  PART 6: grammatical PCA
"""
book_to_parts = read_parts_of_speech_in_chunks(IDEAL_CHUNK_SIZE, MIN_CHUNK_SIZE)
grammar_book_names = list(book_to_parts.keys())
book_to_normalized_part_frequency, parts = calculate_normalized_part_of_speech_ngram_frequencies(
  book_to_parts, NUM_NGRAMS_WANTED, GRAMMAR_NGRAM_SIZE, NORMALIZATION_METHOD)

#generate_scatter_plot(book_to_normalized_part_frequency, grammar_book_names, "Figure 6a: Parts of speech", True, (0.2, -0.2))
#generate_dendrogram(book_to_normalized_part_frequency, grammar_book_names, LINKAGE_ALGORITHM, DISTANCE_METRIC, title='Figure 6b')
plt.show()
plt.close()

grammar_distances = cosine_similarity(book_to_normalized_part_frequency)
grammar_df = pd.DataFrame(grammar_distances, index=grammar_book_names, columns=grammar_book_names)
grammar_df.to_csv('grammar_distances.csv')
