#!/usr/bin/env bash

RUN_UNIT=1
RUN_FUNC=1

if [ "$#" != "0" ]; then
    if [ "$1" == "u" ]; then
        RUN_UNIT=1
        RUN_FUNC=0
        shift
    elif [ "$1" == "f" ]; then
        RUN_UNIT=0
        RUN_FUNC=1
        shift
    fi
fi

if [ $RUN_UNIT == 1 ]; then
    echo "Running unit tests:"
    py.test -c pytest_unit.ini "$@"
fi

if [ $RUN_FUNC == 1 ]; then
    echo "Running functional tests:"
    py.test -c pytest_functional.ini "$@"
fi