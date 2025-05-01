from delta_utils import read_and_calculate_text_to_zscores
from pprint import pprint
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.decomposition import PCA

book_to_word_zscores = read_and_calculate_text_to_zscores(100)
pprint(book_to_word_zscores)

# create DataFrame from dictionary
# where keys are Greek words and values are
# the z-scores (consistently ordered)
word_to_zscores = {}
labels = [] # TODO make sure labels accurate
colors = []
for book, word_zscores in book_to_word_zscores.items():
  for word, zscore in word_zscores.items():
    if word not in word_to_zscores:
      word_to_zscores[word] = []
    word_to_zscores[word].append(zscore)
  labels.append(book)

  if book in ["romans", "1-corinthians", "2-corinthians", "galatians", "philippians", "1-thessalonians", "philemon"]:
    colors.append("b")
  elif book in ["ephesians", "colossians", "2-thessalonians", "1-timothy", "2-timothy", "titus"]:
    colors.append("r")
  else:
    colors.append("g")

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
  ax.annotate(label, (X_reduced[i, 0] + 0.15, X_reduced[i, 1] - 0.2))

plt.show()
