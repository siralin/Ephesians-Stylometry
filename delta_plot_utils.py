import pandas as pd
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA

def display_graph(book_to_word_zscores, label_x_adjustment, label_y_adjustment):

  # create DataFrame from dictionary
  # where keys are Greek words and values are
  # the z-scores (consistently ordered)
  word_to_zscores = {}
  labels = [] # TODO make sure labels accurate
  colors = []
  for book, word_zscores in book_to_word_zscores.items(): # note dicts are insertion-ordered
    for word, zscore in word_zscores.items():
      if word not in word_to_zscores:
        word_to_zscores[word] = []
      word_to_zscores[word].append(zscore)
    labels.append(book)

    if book in UNCONTESTED_PAUL_BOOKS:
      colors.append("b")
    elif book in CONTESTED_PAUL_BOOKS:
      colors.append("r")
    else:
      colors.append("g")

  # DataFrame column order follows dict insertion order
  data = pd.DataFrame(word_to_zscores)

  fig = plt.figure(1, figsize=(8, 6))
  ax = fig.add_subplot(111)

  X_reduced = PCA(n_components=2).fit_transform(data)
  scatter = ax.scatter(
      X_reduced[:, 0],
      X_reduced[:, 1],
      c = colors
  )

  for i, label in enumerate(labels):
    ax.annotate(label, (X_reduced[i, 0] + label_x_adjustment, X_reduced[i, 1] + label_y_adjustment))

  plt.show()
