# from pprint import pprint
# import sys

from switch import switch
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





def action_add(**kwargs):
  pass

def action_remove(**kwargs):
  pass

def action_sub(**kwargs):
  print()

