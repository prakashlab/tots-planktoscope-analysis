#!/bin/bash -eux

archives_root="$1"
processing_dir="$2" # e.g. /home/pi/data
id="$3"

mkdir -p "$processing_dir/import"
cp "$archives_root/$id.tar.gz" "$processing_dir/import/"
tar -xzf "$processing_dir/import/$id.tar.gz" -C "$processing_dir/img"
rm "$processing_dir/import/$id.tar.gz"
