from read_text_utils import read_relevant_texts_in_chunks
from read_nt_text_utils import read_parts_of_speech_in_chunks
from word_utils import calculate_normalized_word_frequencies
from function_word_utils import calculate_normalized_function_word_frequencies, calculate_raw_function_word_frequencies
from scatter_plot_utils import generate_scatter_plot, generate_component_plot
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from sklearn.metrics.pairwise import cosine_similarity
from thesis_paul_markers import graph_paul_markers
from ngram_utils import calculate_normalized_ngram_frequencies
from distance_printer import print_distance_info, print_just_distances
from grammar_utils import calculate_normalized_part_of_speech_ngram_frequencies
from dendrogram_utils import generate_dendrogram
from general_utils import UNCONTESTED_PAUL_BOOKS

"""
Generates figures for the thesis.

PART 1: 500 most common words
"""

IDEAL_CHUNK_SIZE = 3000
MIN_CHUNK_SIZE = 3000

NUM_WORDS_WANTED = 500
NORMALIZATION_METHOD = 'zscore'
NUM_NGRAMS_WANTED = 500
GRAMMAR_NGRAM_SIZE = 1

# for dendrograms
LINKAGE_ALGORITHM = 'average' # best with grammar dendrogram at least
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

#generate_scatter_plot(book_to_normalized_word_frequency, book_to_text.keys(), title="Figure 1a", include_labels=True)
#generate_component_plot(book_to_normalized_word_frequency, words, title="Figure 1b")
#generate_dendrogram(book_to_normalized_word_frequency, book_names, LINKAGE_ALGORITHM, DISTANCE_METRIC, title='Figure 1c')
#plt.show()
#plt.close()

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

#generate_scatter_plot(book_to_normalized_word_frequency, book_to_text.keys(), title="Figure 2a")
#generate_component_plot(book_to_normalized_word_frequency, function_words, title="Figure 2b")
generate_dendrogram(book_to_normalized_word_frequency, book_names, LINKAGE_ALGORITHM, DISTANCE_METRIC, title='Figure 2c')
#plt.show()
#plt.close()

"""
 PART 3: Calculate distances using Cosine Delta
 """
distances = cosine_similarity(book_to_normalized_word_frequency)
df = pd.DataFrame(distances, index=book_names, columns=book_names)
#df.to_csv('distances.csv')
#print_distance_info(distances, book_names, 'Ephesians')

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
generate_dendrogram(book_to_normalized_bigram_frequency, book_names, LINKAGE_ALGORITHM, DISTANCE_METRIC, title='Figure 5c')
#plt.show()
#plt.close()

bigram_distances = cosine_similarity(book_to_normalized_bigram_frequency)
#bigram_df = pd.DataFrame(bigram_distances, index=book_names, columns=book_names)
#bigram_df.to_csv('bigram_distances.csv')
#print_distance_info(bigram_distances, book_names, 'Ephesians')

book_to_normalized_trigram_frequency, trigrams = calculate_normalized_ngram_frequencies(
  book_to_text, NUM_NGRAMS_WANTED, 3, NORMALIZATION_METHOD)
print(trigrams)
#generate_scatter_plot(book_to_normalized_trigram_frequency, book_to_text.keys(), title="Figure 5d (trigrams)")
#generate_component_plot(book_to_normalized_trigram_frequency, trigrams, title="Figure 5e")
generate_dendrogram(book_to_normalized_trigram_frequency, book_names, LINKAGE_ALGORITHM, DISTANCE_METRIC, title='Figure 5f')
#plt.show()
#plt.close()

trigram_distances = cosine_similarity(book_to_normalized_trigram_frequency)
#trigram_df = pd.DataFrame(trigram_distances, index=book_names, columns=book_names)
#trigram_df.to_csv('trigram_distances.csv')
#print_distance_info(trigram_distances, book_names, 'Ephesians')

"""
  PART 6: comparing distances from other books
"""
#print_just_distances(distances, book_names, 'Paul A')
#print_just_distances(distances, book_names, 'Galatians')
#print_just_distances(distances, book_names, '2 Corinthians A') #
#print_just_distances(distances, book_names, 'Romans B')

"""
  PART 7: grammatical PCA
"""
book_to_parts = read_parts_of_speech_in_chunks(IDEAL_CHUNK_SIZE, MIN_CHUNK_SIZE)
grammar_book_names = list(book_to_parts.keys())
book_to_normalized_part_frequency, parts = calculate_normalized_part_of_speech_ngram_frequencies(
  book_to_parts, NUM_NGRAMS_WANTED, GRAMMAR_NGRAM_SIZE, NORMALIZATION_METHOD)
print(parts)

#generate_scatter_plot(book_to_normalized_part_frequency, grammar_book_names, title="Figure 7a (parts of speech)")
#generate_component_plot(book_to_normalized_part_frequency, parts, title="Figure 7b")
generate_dendrogram(book_to_normalized_part_frequency, grammar_book_names, LINKAGE_ALGORITHM, DISTANCE_METRIC, title='Figure 7c')
plt.show()
plt.close()

grammar_distances = cosine_similarity(book_to_normalized_part_frequency)
#grammar_df = pd.DataFrame(grammar_distances, index=grammar_book_names, columns=grammar_book_names)
#grammar_df.to_csv('grammar_distances.csv')
#print_distance_info(grammar_distances, grammar_book_names, 'Ephesians')
