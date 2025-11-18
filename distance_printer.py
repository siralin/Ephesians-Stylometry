from general_utils import UNCONTESTED_PAUL_BOOKS, CONTESTED_PAUL_BOOKS
from statistics import fmean

def print_just_distances(all_distances, text_names, this_text_name):
  this_text_distances = _to_distance_tuples(all_distances, text_names, this_text_name)
  _sort_nearest_first(this_text_distances)
  print('\n')
  print('\n'.join([text_name + ',' + str(dist) for dist, text_name in this_text_distances]))

# all_distances: 2D list.  both columns and rows match up with text_names, in order.
#  the values are the cosine similarities between the texts.
def print_distance_info(all_distances, text_names, this_text_name):
  print_just_distances(all_distances, text_names, this_text_name)

  num_closest_pauline_texts = []
  for text_name in text_names:
    if not _text_is_pauline(text_name):
      continue

    try:
      index = text_names.index(text_name)
    except ValueError:
      print(text_name + ' not found')
      continue # some books not present depending on chunk size

    this_text_distances = _to_distance_tuples(all_distances, text_names, text_name)
    _sort_nearest_first(this_text_distances)
    num_paul = -1
    for dist, other_text in this_text_distances:
      if _text_is_pauline(other_text):
        num_paul += 1
      elif other_text not in CONTESTED_PAUL_BOOKS:
        break
    #print(str(num_paul) + ' books close to ' + text_name)
    num_closest_pauline_texts += [num_paul]

  average = fmean(num_closest_pauline_texts)
  number = len(num_closest_pauline_texts)
  print('Average of ' + str(average) + ' Pauline texts closest to each Pauline text')
  print('That\'s out of ' + str(number) + ' Pauline texts total.')
  print('(' + str(average / number) + '%)')

def _text_is_pauline(text_name):
  return text_name.startswith(tuple(UNCONTESTED_PAUL_BOOKS + ['Paul']))

# distances: list of (distance, text name) tuples
#
# Modifies the input list.
def _sort_nearest_first(distances):
  distances.sort(key=lambda tup: tup[0], reverse=True)

def _to_distance_tuples(all_distances, text_names, text_name):
  return list(zip(all_distances[text_names.index(text_name)], text_names))
