#!/bin/bash

archives_root="$1"
processing_dir="$2" # e.g. /home/pi/data
adjustment="$3" # e.g. 5%
scripts_root="$(dirname "$(realpath "$BASH_SOURCE")")"

echo "Cleaning up..."
sudo $scripts_root/tots-clean.sh "$processing_dir"
while true; do
  next_dataset="$($scripts_root/tots-next-unprocessed-dataset.sh "$archives_root")"
  if [ -z "$next_dataset" ]; then
    sleep 60
    continue
  fi
  echo "Processing dataset $next_dataset..."
  $scripts_root/tots-process-remotely.sh "$archives_root" "$processing_dir" "$next_dataset" "$adjustment"
  echo "Done processing dataset $next_dataset! Waiting for 30 seconds to proceed (press Ctrl+C to quit)..."
  sleep 30
done
