#!/bin/bash -eux

id="$1"
archives_root="/media/pi/Elements/tots-ps/data"
results_target="/home/pi/data/results-preview/$id"

"mkdir -p "$results_target/"
cp "$archives_root/$id-results.tar.gz" "$results_target/"
cd "$results_target"
tar -xzf "$id-results.tar.gz" objects export
rm "$results_target/$id-results.tar.gz"
rclone mkdir "prakashlab-googledrive:/field_work/2023/2023-Arctic-SKQ/Data/PlanktoScope/results-preview/$id"
rclone sync "$results_target" "prakashlab-googledrive:/field_work/2023/2023-Arctic-SKQ/Data/PlanktoScope/results-preview/$id"
