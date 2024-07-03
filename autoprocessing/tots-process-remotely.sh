#!/bin/bash -eux

archives_root="$1"
processing_dir="$2" # e.g. /home/pi/data
id="$3"
adjustment="$4" # e.g. 5%
scripts_root="$(dirname "$(realpath "$BASH_SOURCE")")"

mqtt_api="localhost"
$scripts_root/tots-upload-frames.sh "$archives_root" "$processing_dir" "$id"
$scripts_root/tots-adjust-frames.sh "$processing_dir" "$id" "$adjustment"
planktoscope dev --api mqtt://localhost:1883 proc start
$scripts_root/tots-download-results.sh "$archives_root" "$processing_dir" "$id"
