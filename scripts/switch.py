class switch(object):

  def __init__(self, value):
    self.value = value
    self.fall = False

  def __iter__(self):
    yield self.match
    raise StopIteration

  def match(self, *args):
    if self.fall or not args:
      return True

    if self.value in args:
      self.fall = True
      return True

    return False


class lambda_switch(switch):

  def match(self, test):

    if self.fall or not test:
      return True

    if test(self.value):
      self.fall = True
      return True

    return False


