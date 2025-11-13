from read_text_utils import read_relevant_texts_in_chunks
from word_utils import calculate_normalized_word_frequencies
from function_word_utils import calculate_normalized_function_word_frequencies, calculate_raw_function_word_frequencies
from scatter_plot_utils import generate_scatter_plot, generate_component_plot
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from sklearn.metrics.pairwise import cosine_similarity
from general_plot_utils import get_label_color

"""
Generates figures for the thesis.

PART 1: 500 most common words
"""

MIN_CHUNK_SIZE = 2000

book_to_text = read_relevant_texts_in_chunks(MIN_CHUNK_SIZE)
for book, text in book_to_text.items():
  print(book, len(text.split()))

NUM_WORDS_WANTED = 500
NORMALIZATION_METHOD = 'zscore'

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

book_to_normalized_word_frequency = calculate_normalized_function_word_frequencies(
  book_to_text, function_words, NORMALIZATION_METHOD)

#generate_scatter_plot(book_to_normalized_word_frequency, book_to_text.keys(), title="Figure 2a")
#generate_component_plot(book_to_normalized_word_frequency, function_words, title="Figure 2b")
#plt.show()

# Calculate distances using Cosine Delta
distances = cosine_similarity(book_to_normalized_word_frequency)
book_names = list(book_to_text.keys())
df = pd.DataFrame(distances, index=book_names, columns=book_names)
df.to_csv('distances.csv')

# graph paul markers
colors = [get_label_color(b) for b in book_to_text.keys()]
for word in  ['δε', 'τουτο']:
  frequencies = calculate_raw_function_word_frequencies(book_to_text, [word])

  fig = plt.figure(1, figsize=(8, 6))
  ax = fig.add_subplot()

  bars = zip(book_to_text.keys(), [f[0] for f in frequencies], colors)

  for x, y, color in sorted(bars, key=lambda x: x[1]):
    ax.bar(x, y, color=color)

  plt.xticks(rotation='vertical')
  plt.ylabel('Frequency of usage of ' + word)
  fig.tight_layout()
  #plt.show()
