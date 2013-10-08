import sys, helpers
from pprint import pprint

current_law = ""
for fact in helpers.extract_facts(sys.argv[1]):
  if not current_law and 'Law' in fact:
  	current_law = fact['Law']
  elif 'Law' in fact:
  	raise Exception('Demo version works only with one law in amendment')

  if 'Action' not in fact:
  	continue

  action = helpers.parse_action(fact['Action'])
  action(**fact)


