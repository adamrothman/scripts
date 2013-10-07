#!/bin/sh

# Based on https://github.com/necolas/dotfiles/blob/master/bin/backup

rsync --archive \
      --delete \
      --delete-excluded \
      --exclude-from="$BACKUP_EXCLUDE" \
      --hard-links \
      --one-file-system \
      --progress \
      --sparse \
      --verbose \
      --xattrs \
      "$BACKUP_SOURCE" "$BACKUP_DESTINATION"

exit 0
