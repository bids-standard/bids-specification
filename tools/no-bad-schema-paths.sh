#!/bin/bash

set -eu -o pipefail

cd `readlink -f "$0" | xargs dirname`/../src/schema

grep -oE '(://)?([-_A-Za-z]+\.)+[-_A-Za-z]+' README.md \
    | grep -v -e :// -e '\.\(md\|html\|json\|tsv\|yaml\)$' \
    | grep -e '^\(meta\|objects\|rules\)' \
    | grep -v 'objects.metadata.OtherObjectName' \
    | sort | uniq | \
    while read p; do
        # filepath=${path//.//};
        #echo "$filepath"
        #ls -ld "$filepath"* || echo "nope"
        #echo -n "$path: "
        v=$(jq ".$p" < ../../../bids-schema/versions/master/schema.json | grep -v '^null$' || :)
        if [ -z "$v" ]; then
            echo "$p: not reachable"
        fi
    done
