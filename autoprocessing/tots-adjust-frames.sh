#!/bin/bash -eu

processing_dir="$1" # e.g. /home/pi/data
id="$2"
adjustment="$3" # e.g. 5%

for file in $processing_dir/img/*/*/*/*.jpg; do
  magick "$file" -evaluate add "$adjustment" "$file"
done
