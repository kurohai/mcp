#!/usr/bin/env bash



function datev2(){
    echo $(date +%Y-%m-%d-%H%M)
}


function runner() {
    ./.venv/bin/python ./manage_mastercontrol.py quick --port=9008
}

while sleep 3;
do
    echo "running again $(datev2)"
    find ./ \
        -type f \
        -regextype egrep \
        -not -iregex \
            ".*(/\.*venv/|.git/|data/|archive/|log/|\.py[cod]|\.db).*" |\
    entr -p echo /_ $(datev2) $(runner);
done
