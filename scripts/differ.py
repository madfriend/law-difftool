import os
parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.sys.path.insert(0,parentdir)
from googlediff import diff_match_patch

class differ(diff_match_patch):

  def diff_prettyHtml(self, diffs):
    """Convert a diff array into a pretty HTML report.

    Args:
      diffs: Array of diff tuples.

    Returns:
      HTML representation.
    """
    html = []
    for (op, data) in diffs:
      text = (data.replace("&", "&amp;").replace("<", "&lt;")
                 .replace(">", "&gt;").replace("\n", "<br>"))
      if op == self.DIFF_INSERT:
        html.append("<ins>%s</ins>" % text)
      elif op == self.DIFF_DELETE:
        html.append("<del>%s</del>" % text)
      elif op == self.DIFF_EQUAL:
        html.append("<span>%s</span>" % text)
    return "".join(html)

  def diff_wordsToChars(self, text1, text2, splitter=None):
    import re
    if splitter is None:
      pattern = re.compile(r'\n')
    else:
      pattern = re.compile(splitter)


    lineArray = []
    lineHash = {}

    # "\x00" is a valid character, but various debuggers don't like it.
    # So we'll insert a junk entry to avoid generating a null character.
    lineArray.append('')

    def diff_wordsToCharsMunge(text, pattern):
      """Split a text into an array of strings.  Reduce the texts to a string
      of hashes where each Unicode character represents one line.
      Modifies linearray and linehash through being a closure.

      Args:
        text: String to encode.

      Returns:
        Encoded string.
      """
      chars = []
      # Walk the text, pulling out a substring for each line.
      # text.split('\n') would would temporarily double our memory footprint.
      # Modifying text would create many large strings to garbage collect.
      lineStart = 0
      lineEnd = -1
      while lineEnd < len(text) - 1:

        m = pattern.search(text, lineStart)
        if m:
          lineEnd = m.start()
        else:
          lineEnd = len(text) - 1

        line = text[lineStart:lineEnd + 1]
        lineStart = lineEnd + 1

        if line in lineHash:
          chars.append(chr(lineHash[line]))
        else:
          lineArray.append(line)
          lineHash[line] = len(lineArray) - 1
          chars.append(chr(len(lineArray) - 1))
      return "".join(chars)

    chars1 = diff_wordsToCharsMunge(text1, pattern)
    chars2 = diff_wordsToCharsMunge(text2, pattern)
    return (chars1, chars2, lineArray)


  def diff_charsToWords(self, diffs, lineArray):
    """Rehydrate the text in a diff from a string of line hashes to real lines
    of text.

    Args:
      diffs: Array of diff tuples.
      lineArray: Array of unique strings.
    """
    for x in range(len(diffs)):
      text = []
      for char in diffs[x][1]:
        text.append(lineArray[ord(char)])
      diffs[x] = (diffs[x][0], "".join(text))