#! /bin/sh
# Checks the scripts
# Copyright (C) 2024 kaoru  <https://www.tetengo.org/>

if [ "x$1" = "x" ]; then
    BASEDIR=$(dirname $0)
else
    BASEDIR=$1
fi

echo "Checking $BASEDIR..."
mypy --strict --no-warn-unused-ignores "$BASEDIR"
black --quiet "$BASEDIR"
for f in $BASEDIR/*.py; do
    isort --profile black "$f"
done
