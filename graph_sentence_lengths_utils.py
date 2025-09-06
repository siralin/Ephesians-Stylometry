import os

DIRECTORY = 'netbible_chapters'

def merge_chapters(chapter_list):
  text = ''
  for chapter in chapter_list:
    if chapter is not None:
      text += chapter
  return text

def read_books():
  book_to_chapters = {}

  for filename in os.listdir(DIRECTORY):
    if '-norm' not in filename:
      hyphen_index = filename.index('-', 2) # index of first hyphen after book name
      book = filename[:hyphen_index]
      chapter_number = int(filename[hyphen_index + 1: filename.index('-', hyphen_index + 1)])

      if book not in book_to_chapters:
        book_to_chapters[book] = [None] * 28

      chapter_contents = ''
      with open(os.path.join(DIRECTORY, filename), 'r') as handle:
        for line in handle:
          chapter_contents += line
        # note: chapter may start in middle of sentence; need to combine chapters into books
      book_to_chapters[book][chapter_number - 1] = chapter_contents

  return {book: merge_chapters(chapters) for book, chapters in book_to_chapters.items()}

def count_sentence_lengths(text):
  # TODO remove text in brackets etc from word counts
  # TODO make sure all sentences end in a period or consider alternate punctuation
  # TODO is this an effect of a later punctuator?  could we split up sentences in Ephesians by adding more periods?
  sentences = [sen.split() for sen in text.split('.')]
  normalized_sentences = [[w for w in sentence if not w.isdigit()] for sentence in sentences]
  lengths = [len(sen) for sen in normalized_sentences]

  # Remove data for empty "sentences"
  return [l for l in lengths if l > 0]
