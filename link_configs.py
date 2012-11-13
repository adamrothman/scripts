#!/usr/bin/env python

from argparse import ArgumentParser
from path import path

config_root = path('~').expand() / 'Dropbox' / 'Config'
skip_dirs = set(['alfred', 'oh-my-zsh'])

parser = ArgumentParser(description='Symlink config files into system locations.')
parser.add_argument('-o', '--overwrite', help='overwrite existing files when linking', action='store_true')
args = parser.parse_args()

def link(source, target):
  try:
    source.symlink(target)
    print('New link\t{} -> {}'.format(target, source))
  except OSError as e:
    if args.overwrite:
      target.remove()
      link(source, target)
    else:
      print('Exists\t{}'.format(target))

for d in config_root.dirs('[!.]*'):
  if d.name in skip_dirs:
      continue

  for f in d.listdir('[!.]*'):
    target = path('~').expand()

    if d.name == 'dotfiles':
      target = target / ('.' + f.name)
    elif d.name == 'sublime':
      target = target / 'Library' / 'Application Support' / 'Sublime Text 2' / f.name
    elif d.name == 'preferences':
      target = target / 'Library' / 'Preferences' / f.name

    link(f, target)
