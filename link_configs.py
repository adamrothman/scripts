#!/usr/bin/env python

from argparse import ArgumentParser
from os import remove
from os.path import lexists
from path import path
from shutil import rmtree

parser = ArgumentParser(description='Symlink config files into system locations.')
parser.add_argument('--directory', default='~/Dropbox/Config', help='directory containing config files (defaults to ~/Dropbox/Config)')
parser.add_argument('--dry-run', action='store_true', help='print intended actions instead of actually performing them')
parser.add_argument('--overwrite', action='store_true', help='overwrite existing files when linking')
args = parser.parse_args()

config_root = path(args.directory).expand()
home = path('~').expand()

def listdir_visible(p):
  return [f for f in p.listdir() if not f.name.startswith('.')]

def link(source, target):
  if lexists(target):
    if args.overwrite is False:
      print('Exists\t{}'.format(target))
      return
    else:
      type_to_remove = None
      removal_fn = None
      if target.islink():
        type_to_remove = 'link'
        removal_fn = remove
      elif target.isfile():
        type_to_remove = 'file'
        removal_fn = remove
      elif target.isdir():
        type_to_remove = 'dir'
        removal_fn = rmtree
      if type_to_remove is not None and removal_fn is not None:
        if args.dry_run is True:
          print('Would have removed {}\t{}'.format(type_to_remove, target))
        else:
          removal_fn(target)
          print('Removed {}\t{}'.format(type_to_remove, target))
  if args.dry_run is True:
    print('Would have created link\t{} -> {}'.format(target, source))
  else:
    source.symlink(target)
    print('Created link\t{} -> {}'.format(target, source))

def link_dotfiles():
  for f in listdir_visible(config_root / 'dotfiles'):
    link(f, home / '.{}'.format(f.name))

def link_preferences():
  for f in listdir_visible(config_root / 'preferences'):
    link(f, home / 'Library' / 'Preferences' / f.name)

def link_support():
  for d in listdir_visible(config_root / 'support'):
    for f in listdir_visible(d):
      link(f, home / 'Library' / 'Application Support' / d.name / f.name)

if __name__ == '__main__':
  link_dotfiles()
  link_preferences()
  link_support()
