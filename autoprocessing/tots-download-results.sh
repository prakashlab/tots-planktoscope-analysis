#!/bin/bash -eux

archives_root="$1"
processing_dir="$2" # e.g. /home/pi/data
id="$3"

sudo chown $USER:$USER "$processing_dir"
sudo chown $USER:$USER -R "$processing_dir"
mkdir -p $processing_dir/import
tar -C "$processing_dir" -czf "$processing_dir/results/$id-results.tar.gz" objects/ export/
ls -l $processing_dir/objects/*/*/*/*.jpg | wc -l > "$processing_dir/results/$id-results-count.txt"
cp "$processing_dir/results/$id-results.tar.gz" "$archives_root/"
cp "$processing_dir/results/$id-results-count.txt" "$archives_root/"
rm -rf $processing_dir/clean/*
rm -rf $processing_dir/objects/*
rm -rf $processing_dir/img/*
rm -rf $processing_dir/export/ecotaxa/*
rm "$processing_dir/results/$id-results.tar.gz"
rm "$processing_dir/results/$id-results-count.txt"
