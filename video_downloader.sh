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
  id=$(echo "$line" | cut -f 1 -d $'\t')
  url=$(echo "$line" | cut -f 2 -d $'\t')
  out_path="${out_dir}/${id}.mp4"
  if [ ! -f "$out_path" ]; then
      cmd="wget -q -O ${out_path} ${url}"
      echo "$cmd"
      eval "$cmd"
  fi
done <<< $(cat $in_file \
    | jq -c 'select(.id)' \
    | jq -c 'select(.media.reddit_video.fallback_url)' \
    | jq -c '[.id, .media.reddit_video.fallback_url]' \
    | jq -cr '@tsv'
)
