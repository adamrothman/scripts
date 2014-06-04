#!/bin/sh

# Based on https://github.com/necolas/dotfiles/blob/master/bin/backup

# The --rsync-path argument is specific to my setup and my server, you
# will probably want to remove it if you aren't copying from a remote
# machine and/or that's not where rsync lives on said machine.

rsync --archive \
      --compress \
      --delete \
      --delete-excluded \
      --exclude-from="$BACKUP_EXCLUDE" \
      --hard-links \
      --one-file-system \
      --progress \
      --rsync-path=/opt/bin/rsync \
      --sparse \
      --verbose \
      --xattrs \
      "$BACKUP_SOURCE" \
      "$BACKUP_DESTINATION"

exit 0
