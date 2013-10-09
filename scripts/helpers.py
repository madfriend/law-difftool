# from pprint import pprint
# import sys

from switch import switch
import re
# from SnowballStemmer import Stemmer

def extract_facts(file):
  with open(file) as f:
    buffer = []
    facts = []

    collect_properties = False
    for line in f:
      line = line.strip()

      if line == '{':
        # print("Facts start")
        buffer.pop()
        facts.append({'Lead': "\n".join(buffer)})
        collect_properties = True
        continue

      if line == '}':
        # print("Facts stop")
        collect_properties = False
        buffer = []
        yield facts[-1]
        continue

      if collect_properties:
        # print("Collecting props")
        # print(line.split('='))
        name, value = map(lambda x: x.strip(), line.split('='))
        facts[-1][name] = value
        continue

      # print("Lead")
      buffer.append(line)

  # pprint(facts)


def parse_action(action):

  # st = Stemmer()
  action = action.strip().lower()

  for case in switch(action):
    if case('дополнить'):
      return action_add
    elif case('исключить'):
      return action_remove
    elif case('заменить'):
      return action_sub
    else:
      raise Exception('unknown action')

def normalize_location(string):
  repl = [('вторая', '2'),]
  for (what, to) in repl:
    string = string.replace(what, to)
  return string

def parse_location(string):

  location = {
    'part': '',
    'article': '',
    'after_words': False
  }

  string = normalize_location(string)
  article = re.compile('стать(?:я|и) (\d+)')
  part = re.compile('часть (\d+)')
  after_words = re.compile('после слов')

  location['article'] = int(article.search(string).group(1))
  location['part'] = int(part.search(string).group(1))
  location['after_words'] = True if after_words.findall(string) else False

  return location



def action_add(**kwargs):
  location = kwargs['location']
  source = kwargs['source']

  bounds = find_bounds(location, source)

  loc = bounds[1]
  if (location['after_words']):
    loc = source.find(kwargs['Amend'], bounds[0], bounds[1]) \
    + len(kwargs['Amend'])

  return source[:loc] + ' ' + kwargs['AmendChng'] + ' ' + source[loc:]

def find_bounds(location, source):
  bounds = (source.find('Статья %d'
    % (location['article'],)), source.find('Статья %d'
    % (location['article'] + 1,)))

  p_start = source.find('%d.' % (location['part'],), bounds[0], bounds[1])
  bounds = (p_start,
    source.find('%d.' % (location['part'] + 1, ), p_start, bounds[1]))

  return bounds

def action_remove(**kwargs):
  location = kwargs['location']
  source = kwargs['source']

  bounds = find_bounds(location, source)
  source = source[:bounds[0]] \
     + re.sub('\s+', ' ', source[bounds[0]:bounds[1]]) \
     + source[bounds[1]:]

  loc = source.find(kwargs['Amend'], bounds[0], bounds[1])
  return source[:loc] + source[loc + len(kwargs['Amend']):]

def action_sub(**kwargs):
  location = kwargs['location']
  source = kwargs['source']

  bounds = find_bounds(location, source)
  source = source[:bounds[0]] \
     + re.sub('\s+', ' ', source[bounds[0]:bounds[1]]) \
     + source[bounds[1]:]

  return source[:bounds[0]] \
    + source[bounds[0]:bounds[1]].replace(kwargs['Amend'],
      ' ' + kwargs['AmendChng'] + ' ') \
    + source[bounds[1]:]

