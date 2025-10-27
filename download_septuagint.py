import requests
import time
import os
from bs4 import BeautifulSoup, SoupStrainer

source_code = requests.get('https://sacred-texts.com/bib/sep/index.htm')
soup = BeautifulSoup(source_code.content, 'lxml')

links = []
for link in soup.find_all('a'):
    links.append(link)

book_links = links[6:-5]
for link in book_links:
  url = 'https://sacred-texts.com/bib/sep/' + link['href']
  #print(url)
  time.sleep(10)
  book_source_code = requests.get(url)
  book_soup = BeautifulSoup(book_source_code.content, 'lxml')
  book_title = book_soup.find('body').find('h1').getText()
  chapters = book_soup.find('body').find_all('p')
  chapter_links = [c.find('a') for c in chapters[:-1]]

  print(book_title)
  book_text = ""

  for chapter_link in chapter_links:
    time.sleep(10)
    chapter_source_code = requests.get('https://sacred-texts.com/bib/sep/' + chapter_link['href'])

    paragraphs = BeautifulSoup(chapter_source_code.content, 'lxml').find('body').find_all('p')[:-1]
    for paragraph in paragraphs:
      book_text += paragraph.getText()

  with open(os.path.join('septuagint', book_title[book_title.find(':') + 2:] + ".txt"), 'w') as file:
    file.write(book_text)
# first: <a href="gen.htm">Genesis</a>