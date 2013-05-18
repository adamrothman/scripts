#!/usr/bin/env python

import sys
from argparse import ArgumentParser
from path import path
from send2trash import send2trash
from transmissionrpc import Client, TransmissionError

torrents_root = path('~').expand() / 'Downloads'

parser = ArgumentParser(description='Upload .torrent files to a remote Transmission server.')
parser.add_argument('server', help='URL of Transmission server')
parser.add_argument('user', help='Transmission user')
parser.add_argument('password', help='Transmission password')
if len(sys.argv) != 4:
  parser.print_help()
  sys.exit(-1)
args = parser.parse_args()

torrent_files = torrents_root.glob('*.torrent')
if not torrent_files:
  print('No .torrent files in ~/Downloads')
  sys.exit(-1)  

upload_count = 0
client = Client(address=args.server, user=args.user, password=args.password)
for path in torrent_files:
  print('Adding {}'.format(path.encode('utf-8')))
  try:
    with open(path, 'rb') as torrent_file:
      encoded_file = torrent_file.read().encode('base64')
    torrent = client.add_torrent(encoded_file)
    upload_count += 1
    print('> Started {}'.format(str(torrent).split(None, 1)[1].strip('"')))
    send2trash(path)
    print('> Trashed file')
  except TransmissionError as e:
    print('> {}'.format(e))
  print('')

print('Uploaded {} file{}'.format(upload_count, 's' if upload_count != 1 else ''))
