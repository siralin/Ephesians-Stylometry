from delta_utils import read_and_calculate_text_to_zscores
from pprint import pprint
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import pandas as pd

book_to_word_zscores = read_and_calculate_text_to_zscores(3)
pprint(book_to_word_zscores)

# create pairwise plots (sns.pairplot())

# create DataFrame from dictionary
# where keys are Greek words and values are
# the z-scores (consistently ordered)
word_to_zscores = {}
for book, word_zscores in book_to_word_zscores.items():
  for word, zscore in word_zscores.items():
    if word not in word_to_zscores:
      word_to_zscores[word] = []
    word_to_zscores[word].append(zscore)

data = pd.DataFrame(word_to_zscores)
sns.pairplot(data)

plt.show()
