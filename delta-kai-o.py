from delta_utils import read_and_calculate_text_to_zscores
from pprint import pprint
import matplotlib.pyplot as plt
import numpy as np

book_to_word_zscores = read_and_calculate_text_to_zscores(2)
pprint(book_to_word_zscores)

xpoints = []
ypoints = []
labels = []
for book, zscores in book_to_word_zscores.items():
  xpoints.append(zscores['και'])
  ypoints.append(zscores['ο'])
  labels.append(book)
  print(book + ',' + str(zscores['και']) + ',' + str(zscores['ο']))

fig, ax = plt.subplots()
ax.scatter(np.array(xpoints), np.array(ypoints))

for i, label in enumerate(labels):
  ax.annotate(label, (xpoints[i], ypoints[i]))

plt.show()


