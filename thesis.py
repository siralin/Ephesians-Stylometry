from read_text_utils import read_relevant_texts_in_chunks
from word_utils import calculate_normalized_word_frequencies
from function_word_utils import calculate_normalized_function_word_frequencies, calculate_raw_function_word_frequencies
from scatter_plot_utils import generate_scatter_plot, generate_component_plot
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from sklearn.metrics.pairwise import cosine_similarity
from thesis_paul_markers import graph_paul_markers
from ngram_utils import calculate_normalized_ngram_frequencies
from distance_printer import print_distance_info

"""
Generates figures for the thesis.

PART 1: 500 most common words
"""

MIN_CHUNK_SIZE = 2000
NUM_WORDS_WANTED = 500
NORMALIZATION_METHOD = 'zscore'
NUM_NGRAMS_WANTED = 500

book_to_text = read_relevant_texts_in_chunks(MIN_CHUNK_SIZE)
for book, text in book_to_text.items():
  print(book, len(text.split()))

# words: a List of the most frequent words
#
# book_to_normalized_word_frequency: a 2d List[book index][word index]
# where the book index matches the index of the same book in book_to_word_counts and book_to_text
# and the word index matches the index of the same word in words.
book_to_normalized_word_frequency, words = calculate_normalized_word_frequencies(
  book_to_text, NUM_WORDS_WANTED, NORMALIZATION_METHOD)

print(words)

#generate_scatter_plot(book_to_normalized_word_frequency, book_to_text.keys(), title="Figure 1", include_labels=False)
#plt.show()
#plt.close()

"""
PART 2: remove non-function words and too-short texts
"""

for book, text in list(book_to_text.items()):
  if len(text.split()) < 1500 and book not in ['Ephesians', 'Colossians']:
    del book_to_text[book]

function_words = ['και', 'εν', 'του', 'ο', 'δε', 'το', 'εις', 'της', 'η', 'την', 'γαρ', 'τω', 'των', 'τον', 'αυτου', 'μη', 'οτι', 'ου', 'τα', 'εστιν', 'τη', 'ως', 'ουκ', 'ινα', 'οι', 'ημων', 'υμων', 'δια', 'εκ', 'τους', 'τοις', 'επι', 'ει', 'αλλα', 'υμας', 'αυτων', 'ουν', 'κατα', 'υμιν', 'μου', 'προς', 'απο', 'τις', 'τας', 'αυτω', 'σου', 'παντα', 'τουτο', 'αυτον', 'εαν', 'τι', 'αλλ', 'ημας', 'περι', 'δι', 'ουτως', 'υπο', 'υπερ', 'μετα', 'μεν', 'εγω', 'μοι', 'τε', 'ην', 'ημιν', 'εξ', 'ταις', 'καθως', 'ος', 'αυτοις', 'ταυτα', 'με', 'ων', 'εισιν', 'ουδε', 'ω', 'αυτους', 'αυτος', 'ειναι', 'υμεις', 'ουτε', 'νυν', 'παντες', 'παλιν', 'παντων', 'ημεις', 'σε', 'αυτης', 'ουχ', 'πως', 'επ', 'αυτη', 'μαλλον', 'α', 'αι', 'ον', 'μονον', 'σοι', 'ενωπιον', 'αν', 'οταν', 'ετι', 'παρα', 'πασιν', 'ειτε', 'ιδου', 'αυτο', 'παντας', 'συ', 'εμοι', 'παν', 'εαυτους', 'ωστε', 'ουδεν', 'κατ', 'αυτην', 'συν', 'εστε', 'εσται', 'μετ', 'ειμι', 'ωσπερ', 'διο', 'οτε', 'παντι', 'εμου', 'αυτοι', 'ης', 'πας', 'καθ', 'εφ', 'απ', 'τουτου', 'εσμεν', 'χωρις', 'μηδε', 'πασαν', 'εαυτον', 'ουτος', 'αμην', 'παση', 'τοτε', 'αλληλους', 'τινες', 'πασης', 'τινα', 'εαυτου', 'ουτοι', 'τουτω', 'επει', 'ποτε', 'εαυτοις', 'παντος', 'αυτα', 'καγω', 'ουδεις', 'αρα', 'εως', 'εκαστος', 'τουτων', 'αφ', 'παρ', 'οιτινες', 'εαυτων', 'που', 'πασα', 'πρωτον', 'προ', 'παντοτε', 'ενος', 'μηδεν', 'ηδη', 'καλως', 'οντες', 'οπως', 'ητις', 'πολλοι', 'μεθ', 'πολλα', 'οπου', 'αχρι', 'εμε', 'τουτοις', 'πολλων', 'εαυτω', 'ενα', 'ουχι', 'μητε', 'ουκετι', 'οντα', 'ενι', 'αληθως', 'οσα', 'υπ', 'γε', 'ομοιως', 'εκει', 'ταυτην', 'ουαι', 'μια', 'ητε', 'τουτον', 'νυνι', 'ειτα', 'οθεν', 'πλησιον', 'τριτον', 'μηδεις', 'ετερον', 'εμπροσθεν', 'οσοι', 'μεχρι', 'τινος', 'αρτι', 'οσον', 'μεγα', 'τινι', 'τουτ', 'σεαυτον', 'μαλιστα', 'αμα', 'ναι', 'εγγυς', 'μονος', 'καθαπερ']

# We need to renormalize because we've changed the set of texts.
book_to_normalized_word_frequency = calculate_normalized_function_word_frequencies(
  book_to_text, function_words, NORMALIZATION_METHOD)

#generate_scatter_plot(book_to_normalized_word_frequency, book_to_text.keys(), title="Figure 2a")
#generate_component_plot(book_to_normalized_word_frequency, function_words, title="Figure 2b")
#plt.show()

"""
 PART 3: Calculate distances using Cosine Delta
 """
book_names = list(book_to_text.keys())
distances = cosine_similarity(book_to_normalized_word_frequency)
df = pd.DataFrame(distances, index=book_names, columns=book_names)
#df.to_csv('distances.csv')
print_distance_info(distances, book_names, 'Ephesians')

"""
 PART 4: graph paul markers
"""
# graph_paul_markers(book_to_text)

"""
 PART 5: ngram analysis
 """

# ngrams: a List of the most frequent ngrams
#
# book_to_normalized_ngram_frequency: a 2d List[book index][ngram index]
# where the book index matches the index of the same book in book_to_ngram_counts and book_to_text
# and the ngram index matches the index of the same ngram in ngrams.
book_to_normalized_bigram_frequency, bigrams = calculate_normalized_ngram_frequencies(
  book_to_text, NUM_NGRAMS_WANTED, 2, NORMALIZATION_METHOD)
print(bigrams)
#generate_scatter_plot(book_to_normalized_bigram_frequency, book_to_text.keys(), title="Figure 5a (bigrams)")
#generate_component_plot(book_to_normalized_bigram_frequency, bigrams, title="Figure 5b")
#plt.show()
#plt.close()

bigram_distances = cosine_similarity(book_to_normalized_bigram_frequency)
#bigram_df = pd.DataFrame(bigram_distances, index=book_names, columns=book_names)
#bigram_df.to_csv('bigram_distances.csv')
print_distance_info(bigram_distances, book_names, 'Ephesians')

book_to_normalized_trigram_frequency, trigrams = calculate_normalized_ngram_frequencies(
  book_to_text, NUM_NGRAMS_WANTED, 3, NORMALIZATION_METHOD)
print(trigrams)
#generate_scatter_plot(book_to_normalized_trigram_frequency, book_to_text.keys(), title="Figure 5c (trigrams)")
#generate_component_plot(book_to_normalized_trigram_frequency, trigrams, title="Figure 5d")
#plt.show()
#plt.close()

trigram_distances = cosine_similarity(book_to_normalized_trigram_frequency)
#trigram_df = pd.DataFrame(trigram_distances, index=book_names, columns=book_names)
#trigram_df.to_csv('trigram_distances.csv')
print_distance_info(trigram_distances, book_names, 'Ephesians')