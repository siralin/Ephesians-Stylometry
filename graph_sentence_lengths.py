import graph_sentence_lengths_utils as gslu
import sys

# Read in all the (non-normalized) NT texts,
# so that we have a dictionary of book name to complete text.
# Record the length of each sentence.
# Graph the sentence lengths:
#   x-axis: number of words
#   y-axis: frequency (as a fraction of total sentences in the book)
#   one line per book

book_to_text = gslu.read_books()
book_to_sentence_lengths = {book: gslu.count_sentence_lengths(text) for book, text in book_to_text.items()}
print(book_to_sentence_lengths)

max_lengths = [max(x) for x in book_to_sentence_lengths.values()]
max_length = max(max_lengths)
if max_length != 181:
  print("error: max length is " + str(max_length))
  sys.exit()

# The maximum number of sentences is 181,
# so let's go with twenty buckets, each with a range of 10.

# Find max sentence length.
# Decide on buckets for sentence lengths (1-5 words, 6-10, etc).
# Convert counts to frequencies.
# matplotlib.pyplot.plot()
