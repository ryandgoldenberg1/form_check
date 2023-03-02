#!/bin/bash

usage() {
  echo "$(basename "$0") [-i in_file] [-o out_dir]"
  exit 1
}

in_file=
out_dir=

while getopts ":i:o:" name; do
    case $name in
    i) in_file="$OPTARG";;
    o) out_dir="$OPTARG";;
    *) usage ;;
    esac
done

[ -z "$in_file" ] && usage
[ -z "$out_dir" ] && usage

mkdir -p $out_dir
while read line; do
  echo "$line"
  $line
done <<< $(cat $in_file \
    | jq -c 'select(.id)' \
    | jq -c 'select(.media.reddit_video.fallback_url)' \
    | jq -c '{id:.id, url:.media.reddit_video.fallback_url}' \
    | jq -r "\"wget -q -O ${out_dir}/\\(.id).mp4 \\(.url)\""
)
