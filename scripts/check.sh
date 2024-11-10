#! /bin/sh
# Checks the scripts
# Copyright (C) 2024 kaoru  <https://www.tetengo.org/>

if [ "x$1" = "x" ]; then
    BASEDIR=$(dirname $0)
else
    BASEDIR=$1
fi

for f in $BASEDIR/*.py; do
    echo "Checking $(basename $f)..."
    mypy "$f"
    black "$f"
    isort --profile black "$f"
done
