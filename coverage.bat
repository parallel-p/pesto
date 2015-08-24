@echo off
coverage.exe run --rcfile=.coveragerc testing_global.py
coverage.exe html -d coverage/

py.exe test_coverage.py
python test_coverage.py

start coverage/index.html
