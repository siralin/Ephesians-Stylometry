from delta_utils import read_and_calculate_text_to_zscores
from delta_plot_utils import display_graph
from pprint import pprint
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.decomposition import PCA

for i in range(2, 100):
  book_to_word_zscores = read_and_calculate_text_to_zscores(i)
  display_graph(book_to_word_zscores, 0, 0, title="i=" + str(i))
