#!/bin/sh
coverage run --omit "/usr/*" --rcfile=.coveragerc testing_global.py
coverage html -d coverage/
