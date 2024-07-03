#!/bin/bash

archives_root="$1"

files=$(ls -v1 "$archives_root")
results=$(echo "$files" | grep -i '^tots-ps-acq-.*-results.tar.gz$')
for dataset in $(echo "$files" | grep -i '^tots-ps-acq-.*.tar.gz$' | grep -v '^tots-ps-acq-.*-results.tar.gz$'); do
  dataset_name="${dataset%'.tar.gz'}"
  results_name="$dataset_name-results.tar.gz"
  if grep "^$results_name$" <<< "$results" > /dev/null; then
    continue
  fi
  echo "$dataset_name"
  break
done
