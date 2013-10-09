import sys, helpers, re
from pprint import pprint
from differ import differ

current_law = ""
location = ""

with open(sys.argv[2]) as doc:
	source = doc.read()
	original = source
try:
  for fact in helpers.extract_facts(sys.argv[1]):
    if not current_law and 'Law' in fact:
    	current_law = fact['Law']
    elif 'Law' in fact:
    	raise Exception('Demo version works only with one law in amendment')

    if 'Article' in fact and 'Action' not in fact:
    	location = fact['Article']

    if 'Action' not in fact:
    	continue

    action = helpers.parse_action(fact['Action'])
    if ('Article' not in fact): fact['Article'] = ''
    loc = helpers.parse_location(location + ' '
    	+ fact['Article'])

    source = action(location = loc, source = source, **fact)

except Exception as e:
  print(e)

differ = differ()

t1, t2, wordarray = differ.diff_wordsToChars(original, source, splitter=r'\s+');
diffs = differ.diff_main(t1, t2, False);
differ.diff_charsToWords(diffs, wordarray);

# diffs = differ.diff_main(original, source)
differ.diff_cleanupSemantic(diffs)
diffs = [diff for diff in diffs if not re.match('^\s+$', diff[1])]

print(differ.diff_prettyHtml(diffs))