#!/bin/sh

unset WGMDEVELOPMENT
export WGMTESTING=1

./wgm_search_tests.py
#./runserver.py
