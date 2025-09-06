import graph_sentence_lengths_utils as gslu
import sys
import matplotlib.pyplot as plt

# Read in all the (non-normalized) NT texts,
# so that we have a dictionary of book name to complete text.
# Record the length of each sentence.
# Graph the sentence lengths:
#   x-axis: number of words (bucketed)
#   y-axis: frequency (as a fraction of total sentences in the book)
#   one line per book

book_to_text = gslu.read_books()
book_to_sentence_lengths = {book: gslu.count_sentence_lengths(text) for book, text in book_to_text.items()}
print(book_to_sentence_lengths)

# Find max sentence length.
# Decide on buckets for sentence lengths (1-5 words, 6-10, etc).
max_lengths = [max(x) for x in book_to_sentence_lengths.values()]
max_length = max(max_lengths)
if max_length != 181:
  print("error: max length is " + str(max_length))
  sys.exit()

# The maximum number of sentences is 181,
# so let's go with twenty buckets, each with a range of 10.

# Convert counts to frequencies.
# matplotlib.pyplot.plot()

fig = plt.figure()
ax = fig.add_axes([0.1, 0.1, 0.8, 0.8])

for book, sentence_lengths in book_to_sentence_lengths.items():
  num_sentences = len(sentence_lengths)

  # desired format: list of number of sentences (divided by total sentences) in each bucket
  buckets = [0] * 19
  for sentence_length in sentence_lengths:
    buckets[(sentence_length - 1) // 10] += 1
  frequency_buckets = [b / num_sentences for b in buckets]
  print(book, frequency_buckets)

  ax.plot(range(1, 20), frequency_buckets)

plt.show()
