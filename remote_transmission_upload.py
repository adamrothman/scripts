#!/usr/bin/env python3

import sys
from argparse import ArgumentParser

from blessings import Terminal
from path import path
from send2trash import send2trash
from transmissionrpc import Client, TransmissionError

if __name__ == '__main__':
  parser = ArgumentParser(description='Upload .torrent files to a Transmission server.')
  file_group = parser.add_argument_group('file arguments')
  file_group.add_argument('-d', '--directory', default='~/Downloads', help='directory to search for .torrent files (defaults to ~/Downloads)')
  file_group.add_argument('-k', '--keep', action='store_true', help='do not trash .torrent files after uploading')
  server_group = parser.add_argument_group('server arguments')
  server_group.add_argument('--host', required=True, help='Transmission host')
  server_group.add_argument('--port', type=int, default=9091, help='Transmission port (defaults to 9091)')
  server_group.add_argument('--user', required=True, help='Transmission user')
  server_group.add_argument('--password', required=True, help='Transmission password')
  args = parser.parse_args()
  
  t = Terminal()

  directory = path(args.directory).expand()
  print('\nScanning {} for {} files...'.format(t.bold(directory), t.bold('.torrent')), end='')
  torrent_files = directory.files('*.torrent')
  if torrent_files:
    print(t.bold_bright_green(' Found {}'.format(len(torrent_files))))
  else:
    print(t.bold_bright_red(' None found'))
    sys.exit(-1)

  client = Client(address=args.host, port=args.port, user=args.user, password=args.password)
  uploaded, failed = [], []

  # pad the index so that the brackets are all vertically aligned
  width = len(str(len(torrent_files)))

  for i, f in enumerate(torrent_files):
    prefix = ('[{:>' + str(width) + '}]').format(i + 1)
    print('\n' + t.bold(prefix + ' Uploading') + '\t' + f.name)
    try:
      torrent = client.add_torrent('file://' + f)
      uploaded.append(f)
      print(t.bold_bright_green(prefix + ' Started') + '\t' + t.bright_cyan(torrent.name))
    except TransmissionError as e:
      failed.append(f)
      print(t.bold_bright_red(prefix + ' Error') + '\t' + t.bright_black(str(e)))

  if not args.keep:
    # convert to list to force iteration
    list(map(send2trash, uploaded))

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
