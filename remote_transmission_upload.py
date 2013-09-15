#!/usr/bin/env python

import sys
from argparse import ArgumentParser
from path import path
from send2trash import send2trash
from transmissionrpc import Client, TransmissionError

parser = ArgumentParser(description='Upload .torrent files to a Transmission server.')
parser.add_argument('-d', '--directory', default='~/Downloads', help='directory to search for .torrent files (defaults to ~/Downloads)')
server_group = parser.add_argument_group('Transmission server arguments')
server_group.add_argument('--host', required=True, help='Transmission host')
server_group.add_argument('--port', type=int, default=9091, help='Transmission port (defaults to 9091)')
server_group.add_argument('--user', required=True, help='Transmission user')
server_group.add_argument('--password', required=True, help='Transmission password')
args = parser.parse_args()

if __name__ == '__main__':
  directory = path(args.directory).expand()
  torrent_files = directory.files('*.torrent')
  if not torrent_files:
    print('No .torrent files found in {}'.format(directory))
    sys.exit(-1)

  client = Client(address=args.host, port=args.port, user=args.user, password=args.password)
  upload_count = 0
  for path in torrent_files:
    print('Adding {}'.format(path.encode('utf-8')))
    try:
      torrent = client.add_torrent('file://' + path)
      upload_count += 1
      print('> Started {}'.format(str(torrent).split(None, 1)[1].strip('"')))
      send2trash(path)
      print('> Trashed file')
    except TransmissionError as e:
      print('> {}'.format(e))
    print('')

  print('Uploaded {} file{}'.format(upload_count, 's' if upload_count != 1 else ''))
