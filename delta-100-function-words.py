from delta_utils import read_and_calculate_text_to_zscores, display_graph
from pprint import pprint
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.decomposition import PCA

book_to_word_zscores = read_and_calculate_text_to_zscores(100)
pprint(book_to_word_zscores)

display_graph(book_to_word_zscores, 0.15, -0.2)
