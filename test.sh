#!/usr/bin/env bash

echo "Running unit tests:"
py.test -c pytest_unit.ini "$@"

echo "Running functional tests:"
py.test -c pytest_functional.ini "$@"
