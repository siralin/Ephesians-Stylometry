from delta_utils import find_zscores_for_given_words
from delta_plot_utils import display_graph
from pprint import pprint
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.decomposition import PCA

function_words = ['και', 'ο', 'εν', 'δε', 'του', 'εις', 'το', 'τον', 'την', 'η', 'αυτου', 'της', 'τω', 'οτι', 'των', 'οι', 'γαρ', 'μη', 'αυτον', 'εστιν', 'τη', 'αυτω', 'τα', 'ουκ', 'ου', 'τους', 'προς', 'εκ', 'επι', 'ινα', 'τοις', 'υμιν', 'ει', 'αυτοις', 'υμων', 'μου', 'αυτων', 'δια', 'ουν', 'ως', 'απο', 'σου', 'τι', 'αλλα', 'υμας', 'ην', 'τις', 'ημων', 'αυτους', 'τας', 'εγω', 'εαν', 'περι', 'κατα', 'τουτο', 'με', 'μετα', 'εξ', 'μοι', 'υμεις', 'τε', 'αλλ', 'ταυτα', 'σοι', 'ος', 'ταις', 'ουτως', 'υπο', 'αυτη', 'σε', 'ουτος', 'μεν', 'καθως', 'ον', 'αν', 'συ', 'αυτος', 'ημας', 'ημιν', 'εισιν', 'αι', 'υπερ']

# removed: 'θεου', 'ειπεν', 'ιησους', 'ιησου', 'θεος', 'παντα', 'χριστου', 'κυριου', 'λεγω', 'ιδου', 'εγενετο', 'παντες', 'λεγων', 'κυριος', 'πνευμα', 'υιος', 'θεω','λεγει',

# TODO something said to remove pronouns as well, because some things are first person and some are third

book_to_word_zscores = find_zscores_for_given_words(function_words)
display_graph(book_to_word_zscores, 0, 0)
