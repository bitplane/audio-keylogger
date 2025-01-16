#!/bin/sh

set -e

now=$(date -u "+%Y-%m-%dT%H:%M:%SZ" | tr ':' '-' | tr 'T' '_' | tr -d 'Z')

tar -czf data/"$now".tar.gz recordings/*.json recordings/*.wav

rm -r recordings/*.wav recordings/*.json
