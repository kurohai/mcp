#!/usr/bin/env bash


COMMAND=$@

while sleep 3;
do
    echo "running again $(d2)"
    find ./ \
        -type f \
        -regextype egrep \
        -not -iregex \
            ".*(/\.*venv/|.git/|data/|archive/|log/|\.py[cod]|\.db).*" |\
    entr -p echo /_ $(d2) $($COMMAND);
done


# -regextype egrep -not -iregex ".*
