@echo off
coverage.exe run testing_global.py
coverage.exe html -d coverage/

py.exe test_coverage.py
python test_coverage.py

start coverage/index.html
