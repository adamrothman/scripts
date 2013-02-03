#!/usr/bin/env python

from argparse import ArgumentParser
from os import listdir, remove, symlink
from os.path import basename, expanduser, isdir, isfile, islink, join, lexists
from shutil import rmtree

config_root = join(expanduser('~'), 'Dropbox', 'Config')
skip_dirs = set(['alfred', 'oh-my-zsh'])

parser = ArgumentParser(description='Symlink config files into system locations.')
parser.add_argument('-o', '--overwrite', help='overwrite existing files when linking', action='store_true')
args = parser.parse_args()

def link(source, target):
  if lexists(target):
    if not args.overwrite:
      print('Exists\t{}'.format(target))
      return
    else:
      if islink(target):
        remove(target)
        print('Removed link\t{}'.format(target))
      elif isfile(target):
        remove(target)
        print('Removed file\t{}'.format(target))
      elif isdir(target):
        rmtree(target)
        print('Removed dir\t{}'.format(target))
  symlink(source, target)
  print('Created link\t{} -> {}'.format(target, source))

if __name__ == '__main__':
  for d in listdir(config_root):
    d_path = join(config_root, d)
    if d[0] == '.' or not isdir(d_path) or d in skip_dirs:
      continue
    for f in listdir(d_path):
      f_path = join(d_path, f)
      if f[0] == '.':
        continue
      target = expanduser('~')
      if d == 'dotfiles':
        target = join(target, '.' + f)
      elif d == 'sublime':
        target = join(target, 'Library', 'Application Support', 'Sublime Text 2', f)
      elif d == 'preferences':
        target = join(target, 'Library', 'Preferences', f)
      link(f_path, target)
