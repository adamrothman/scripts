# scripts
Some useful scripts I've written along the way.


### backup.sh
A wrapper around `rsync` with some useful options set. It requires you to set three environment variables. I do it in my shell profile, but you can do so anywhere:

- `BACKUP_EXCLUDE` file containing patterns (one per line) to exclude
- `BACKUP_SOURCE` directory to back up
- `BACKUP_DESTINATION` desired backup location


### remote_transmission_upload.py
A Python 3 script that uploads all .torrent files in a directory (`~/Downloads` by default) to a Transmission server. Depends on the following packages, all of which can be installed with `pip3`:

- `blessings`
- `path.py`
- `send2trash`
- `transmissionrpc`

Run the script with `--help` to see the available options.
