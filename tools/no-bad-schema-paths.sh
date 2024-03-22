#!/bin/bash

set -eu -o pipefail

schema_json=$(readlink -f "$1")

cd "$(dirname "$(readlink -f "$0")")/../src/schema"

# Create a temporary file and ensure it gets deleted on exit
tmpfile=$(mktemp)
trap 'rm -f "$tmpfile"' EXIT

grep -oE '(://)?([-_A-Za-z]+\.)+[-_A-Za-z]+' README.md \
    | grep -v -e :// -e '\.\(md\|html\|json\|tsv\|yaml\)$' \
    | grep -e '^\(meta\|objects\|rules\)' \
    | grep -v 'objects.metadata.OtherObjectName' \
    | sort | uniq | \
    while IFS= read -r p; do
        v=$(jq ".$p" < "$schema_json" | grep -v '^null$' || echo "fail")
        if [ -z "$v" ] || [ "$v" = "fail" ]; then
            echo "$p: not reachable" >> "$tmpfile"
        fi
    done

# Check if the temporary file is empty
if [ -s "$tmpfile" ]; then
    cat "$tmpfile" # Display the not reachable paths
    exit 1
fi
