#!/usr/bin/env python

from argparse import ArgumentParser
from os import listdir, remove, symlink
from os.path import basename, expanduser, isdir, isfile, islink, join, lexists
from shutil import rmtree

user_home = expanduser('~')
config_root = join(user_home, 'Dropbox', 'Config')

parser = ArgumentParser(description='Symlink config files into system locations.')
parser.add_argument('-o', '--overwrite', help='overwrite existing files when linking', action='store_true')
args = parser.parse_args()

def listdir_visible(path):
  return [f for f in listdir(path) if f[0] != '.']

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

def link_dotfiles():
  source = join(config_root, 'dotfiles')
  for f in listdir_visible(source):
    link(join(source, f), join(user_home, '.' + f))

def link_preferences():
  source = join(config_root, 'preferences')
  for f in listdir_visible(source):
    link(join(source, f), join(user_home, 'Library', 'Preferences', f))

def link_support():
  source = join(config_root, 'support')
  for d in listdir_visible(source):
    d_path = join(source, d)
    for f in listdir_visible(d_path):
      link(join(d_path, f), join(user_home, 'Library', 'Application Support', d, f))

if __name__ == '__main__':
  link_dotfiles()
  link_preferences()
  link_support()
