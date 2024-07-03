#!/bin/bash -eux

processing_dir="$1" # e.g. /home/pi/data

rm -f $processing_dir/import/*.tar.gz
rm -rf $processing_dir/clean/*
rm -rf $processing_dir/objects/*
rm -rf $processing_dir/img/*
rm -rf $processing_dir/export/ecotaxa/*
rm -f $processing_dir/results/*-results.tar.gz
rm -f $processing_dir/results/*-results-count.txt
rm -f $processing_dir/results-preview/*/*-results.tar.gz
