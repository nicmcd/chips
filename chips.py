#!/usr/bin/env python3

import argparse
import chipdb
import chipplot
import os

db = None

def add(args):
  chip = dict((attr, vars(args)[attr]) for attr in chipdb.ATTRS.keys())
  db.add(overwrite=args.overwrite, **chip)
  db.dump(args.file)

def remove(args):
  chip = dict((attr, vars(args)[attr]) for attr in chipdb.ATTR_ID)
  db.remove(passive=args.passive, **chip)
  db.dump(args.file)

def show(args):
  global db
  if args.filter:
    db = db.filter(args.filter)
  if args.sort:
    db = db.sort(args.sort)
  print(db)

def plot(args):
  global db
  if args.filter:
    db = db.filter(args.filter)
  if args.sort:
    db = db.sort(args.sort)
  chipplot.plot_bandwidth(db, args.plotfile)

if __name__ == '__main__':
  parser = argparse.ArgumentParser(description='Router Chips tool')
  parser.add_argument('-f', '--file', default='chips.db',
                      help='the chips database file')
  parser.add_argument('-v', '--verbose', action='store_true',
                      help='enable verbose output')
  subparsers = parser.add_subparsers(
    dest='COMMAND',
    title='commands',
    description=('A command to be used on the chip database'),
    help='command to be run')
  subparsers.required = True  # HACK TO FIX Python3.3+ bug

  # 'add' chip command
  cmd = 'add'
  add_parser = subparsers.add_parser(cmd,
                                     help='add a chip to the database')
  add_parser.set_defaults(func=add)
  add_parser.add_argument('-o', '--overwrite', action='store_true',
                          help='overwrite existing if exists')
  add_parser.add_argument('company', help='chip company')
  add_parser.add_argument('chipname', help='chip name')
  add_parser.add_argument('year', help='chip release year')
  add_parser.add_argument('bandwidth', help='chip I/O bandwidth')

  # 'remove' chip command
  cmd = 'remove'
  remove_parser = subparsers.add_parser(cmd,
                                        help='remove a chip from the database')
  remove_parser.set_defaults(func=remove)
  remove_parser.add_argument('-p', '--passive', action='store_true',
                             help='ignore if it doesn\'t already exist')
  remove_parser.add_argument('company', help='chip company')
  remove_parser.add_argument('chipname', help='chip name')

  # 'show' chip(s) command
  cmd = 'show'
  show_parser = subparsers.add_parser(cmd,
                                      help='show chips in the database')
  show_parser.set_defaults(func=show)
  show_parser.add_argument('-f', '--filter',
                           help='ex: "p;company;.*Cray.*|n;year;2008;2010"')
  show_parser.add_argument('-s', '--sort',
                           help='sorts: "d;company;chipname" decending')

  # 'plot' chip bandwidths command
  cmd = 'plot'
  plot_parser = subparsers.add_parser(cmd,
                                      help='plot chip bandwidths')
  plot_parser.set_defaults(func=plot)
  plot_parser.add_argument('-f', '--filter',
                           help='ex: "p;company;.*Cray.*|n;year;2008;2010"')
  plot_parser.add_argument('-s', '--sort',
                           help='sorts: "d;company;chipname" decending')
  plot_parser.add_argument('plotfile',
                           help='the plotfile to be written')

  # parse the command line
  args = parser.parse_args()

  # create and load the database
  db = chipdb.ChipDB(verbose=args.verbose)
  if os.path.isfile(args.file):
    db.load(args.file)

  # run the command function
  args.func(args)
