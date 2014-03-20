#!/usr/bin/env python3
import sys
from argparse import ArgumentParser
from getpass import getpass, getuser
from os.path import expanduser, expandvars, normpath
from pathlib import Path

from blessings import Terminal
from send2trash import send2trash
from transmissionrpc import Client, TransmissionError


def upload_torrents():
  parser = ArgumentParser(description='Upload .torrent files to a Transmission server.')

  parser.add_argument('host', type=str, help='Transmission host[:port] (port defaults to 9091)')

  parser.add_argument('-u', '--user', type=str, default=getuser(), help='Transmission username (defaults to current user)')
  parser.add_argument('-d', '--directory', type=str, default='~/Downloads', help='directory to search for .torrent files (defaults to ~/Downloads)')
  parser.add_argument('-k', '--keep', action='store_true', help='do not trash .torrent files after uploading')

  args = parser.parse_args()
  t = Terminal()

  directory = Path(normpath(expanduser(expandvars(args.directory)))).resolve()
  print('\nScanning {} for {} files...'.format(t.bold(str(directory)), t.bold('.torrent')), end='')
  torrent_files = sorted(directory.glob('*.torrent'))
  if torrent_files:
    print(t.bold_bright_green(' Found {}'.format(len(torrent_files))))
  else:
    print(t.bold_bright_red(' None found'))
    return

  password = getpass('\n{}\'s password: '.format(t.bold(args.user)))

  try:
    if ':' in args.host:
      hostname, port = args.host.split(':')
      client = Client(address=hostname, port=port, user=args.user, password=password)
    else:
      client = Client(address=args.host, user=args.user, password=password)
    print(t.bold_bright_green('Connected'))
  except TransmissionError as e:
    print(t.bold_bright_red('Connection failed') + ' to Transmission at ' + t.bold(args.host))
    return

  uploaded, failed = [], []

  # pad the index so that the brackets are all vertically aligned
  width = len(str(len(torrent_files)))

  for i, f in enumerate(torrent_files):
    prefix = ('[{:>{width}}]').format(i + 1, width=width)
    print('\n' + t.bold(prefix + ' Uploading') + '\t' + f.name)
    try:
      torrent = client.add_torrent('file://' + str(f))
      uploaded.append(f)
      print(t.bold_bright_green(prefix + ' Started') + '\t' + t.bright_cyan(torrent.name))
    except TransmissionError as e:
      failed.append(f)
      print(t.bold_bright_red(prefix + ' Error') + '\t' + t.bright_black(str(e)))

  if not args.keep:
    # convert to list to force iteration
    trash = lambda f: send2trash(str(f))
    list(map(trash, uploaded))

  print('')

  if uploaded:
    print('{} file{} uploaded successfully{}'.format(
      t.bold_bright_green(str(len(uploaded))),
      's' if len(uploaded) != 1 else '',
      ' and moved to trash' if not args.keep else ''
    ))

  if failed:
    print('{} file{} failed to upload'.format(
      t.bold_bright_red(str(len(failed))),
      's' if len(failed) != 1 else ''
    ))


if __name__ == '__main__':
  upload_torrents()
