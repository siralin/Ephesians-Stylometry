
# Returns a copy of the given dictionary, broken up so that all texts are less than
# 2 * chunk_size words long.
def break_into_chunks(book_to_text, chunk_size):
  chunked_book_to_text = {}
  for book, text in book_to_text.items():
    chunked_book_to_text.update(_break_up(book, text, chunk_size))
  return chunked_book_to_text

# Returns a copy of the given text, broken up so that all chunks are less than
# 2 * chunk_size words long.
def _break_up(book, text, chunk_min_size):
  words = text.split()
  num_words = len(words)
  num_chunks = num_words // chunk_min_size
  if (num_chunks <= 1):
    return {book: text} # No breaking necessary

  chunk_actual_size = num_words // num_chunks

  broken_book_to_text = {}
  label = ord('A')
  for chunk_index in range(num_chunks): # 0, 1, ...
    end_index = (chunk_index + 1) * chunk_actual_size
    if (chunk_index == num_chunks - 1):
      end_index = None # Include any leftover words at the end

    text_chunk = words[chunk_index * chunk_actual_size:end_index]
    broken_book_to_text[book + ' ' + chr(label)] = ' '.join(text_chunk)
    label += 1

  return broken_book_to_text
