import functools
import json
import operator
import re

# these are all the attributes and types for a chip
ATTRS = {
  'company': str,
  'chipname': str,
  'year': int,
  'bandwidth': float
}

# a comparison function for chips
#  first compares company, then compares year, then compares chipname
def compareChips(chip1, chip2):
  if chip1['company'] < chip2['company']:
    return -1
  elif chip1['company'] > chip2['company']:
    return 1
  else:
    if chip1['year'] < chip2['year']:
      return -1
    elif chip1['year'] > chip2['year']:
      return 1
    else:
      if chip1['chipname'] < chip2['chipname']:
        return -1
      elif chip1['chipname'] > chip2['chipname']:
        return 1
      else:
        return 0

# these attributes represent the unique identifier for a chip
ATTR_ID = ['company', 'chipname']

class ChipDB(object):

  def __init__(self, verbose=False):
    self.chips = []
    self.verbose = verbose

  def add(self, overwrite=False, **chip):
    if self.verbose:
      print('adding {0}'.format(chip))

    # check that chip has all the proper attrs
    for attr in ATTRS.keys():
      assert attr in chip, '{0} missing in {1}'.format(attr, chip)
    for attr in chip:
      assert attr in ATTRS.keys(), '{0} is unknown in {1}'.format(attr, chip)

    # convert keys to proper types
    for attr in ATTRS.keys():
      chip[attr] = ATTRS[attr](chip[attr])

    if not overwrite:
      # check that new chip isn't already in DB
      assert_msg = '{0} already exists in database'.format(chip)
      assert (chip['company'], chip['chipname']) not in self, assert_msg

    else:
      # remove is already in database
      self.remove(passive=True, **chip)

    # add to list
    self.chips.append(chip)

  def remove(self, passive=False, **chip):
    if self.verbose:
      print('removing {0}'.format(chip))

    # remove is already in database
    rm_index = None
    for index, echip in enumerate(self.chips):
      if (chip['company'] == echip['company'] and
          chip['chipname'] == echip['chipname']):
        rm_index = index
        break

    if not rm_index and not passive:
      raise ValueError('{0} does not exist'.format(chip))

    if rm_index:
      del self.chips[rm_index]

  def load(self, filename):
    # load the chips
    if self.verbose:
      print('loading from {0}'.format(filename))
    with open(filename, 'r') as fd:
      chips = json.load(fd)
    for chip in chips:
      self.add(**chip)

    # sort the chips
    self.chips.sort(key=functools.cmp_to_key(compareChips))

  def dump(self, filename):
    # sort the chips
    self.chips.sort(key=functools.cmp_to_key(compareChips))

    # write the chips
    if self.verbose:
      print('dumping to {0}'.format(filename))
    with open(filename, 'w') as fd:
      json.dump(self.chips, fd)

  def filter(self, specs):
    spec = specs.split('|')[0]
    rest = '|'.join(specs.split('|')[1:])

    elems = spec.split(';')
    assert_msg = '"{0}" doesn\'t contain 3 or 4 elements'.format(spec)
    assert len(elems) == 3 or len(elems) == 4, assert_msg

    assert elems[0] == 'p' or elems[0] == 'n', 'needs to start with p or n'
    reverse = elems[0] == 'n'

    field = elems[1]
    assert field in ATTRS.keys(), '"{0}" is not a valid attribute'.format(field)

    if len(elems) == 3:
      match = elems[2]
      newdb = self.filter_match(field, match, reverse=reverse)
      if rest:
        newdb = newdb.filter(rest)
      return newdb
    else:  # len(elems) == 4
      fmin = float(elems[2])
      fmax = float(elems[3])
      newdb = self.filter_range(field, fmin, fmax, reverse=reverse)
      if rest:
        newdb = newdb.filter(rest)
      return newdb

  def filter_match(self, field, match, reverse=False):
    def field_match(x):
      if ATTRS[field] == str:
        # do regex for strings
        return not reverse if re.match(match, x[field]) else reverse
      else:
        # do straight comparison for everything else
        return not reverse if ATTRS[field](match) == x[field] else reverse
    db = ChipDB()
    db.chips = list(filter(field_match, self.chips))
    return db

  def filter_range(self, field, fmin, fmax, reverse=False):
    def field_range(x):
      return not reverse if x[field] >= fmin and x[field] <= fmax else reverse
    db = ChipDB()
    db.chips = list(filter(field_range, self.chips))
    return db

  def sort(self, spec):
    elems = spec.split(';')
    assert len(elems) >= 2, '"{0}" doesn\'t contain 2 elements'.format(spec)

    assert elems[0] == 'a' or elems[0] == 'd', 'needs to start with a or d'
    reverse = elems[0] == 'd'

    fields = elems[1:]
    for field in fields:
      assert_msg = '"{0}" is not a valid attribute'.format(field)
      assert field in ATTRS.keys(), assert_msg

    db = ChipDB()
    db.chips = sorted(self.chips, key=operator.itemgetter(*fields),
                      reverse=reverse)
    return db

  def __contains__(self, testchip):
    for chip in self.chips:
      if chip['company'] == testchip[0] and chip['chipname'] == testchip[1]:
        return True
    return False

  def __str__(self):
    return json.dumps(self.chips, indent=2)

  def matrix(self):
    m = {}
    for attr in ATTRS.keys():
      m[attr] = []
    for chip in self.chips:
      for attr in ATTRS.keys():
        m[attr].append(chip[attr])
    return m
