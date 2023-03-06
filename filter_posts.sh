#!/bin/bash

usage() {
  echo "$(basename "$0") [-i in_file] [-o out_file] [-h video_height] [-e exercise] [-l max_video_length]"
  exit 1
}


in_file=
out_file=
video_height=
exercise=
max_video_length=

while getopts ":i:o:h:e:l:" name; do
    case $name in
    i) in_file="$OPTARG";;
    o) out_file="$OPTARG";;
    h) video_height="$OPTARG";;
    e) exercise="$OPTARG";;
    l) max_video_length="$OPTARG";;
    *) usage ;;
    esac
done

[ -z "$in_file" ] && echo "in_file required" && usage
[ -z "$out_file" ] && echo "out_file required" && usage

if [ ! -z "$exercise" ]; then
    exercise="$(tr '[:lower:]' '[:upper:]' <<< ${exercise:0:1})${exercise:1}"
fi

cat $in_file | \
    ( [ ! -z "$video_height" ] && jq -c "select(.media.reddit_video.height == $video_height)" || cat ) | \
    ( [ ! -z "$exercise" ] && jq -c "select(.link_flair_text == $exercise)" || cat ) | \
    ( [ ! -z "$max_video_length" ] && jq -c "select(.media.reddit_video.duration <= $max_video_length)" || cat )
