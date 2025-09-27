
# Returns the given text with all punctuation removed.
# All returned characters will be capital Greek letters or spaces.
def normalize(text):
  result = text.upper().replace('.', '').replace(';', '')

  # check all resulting characters to make sure they're simple greek letters
  for c in result:
    if ord(c) not in range(913, 938) and c != ' ':
      print('ERROR:' + c)

  return result
