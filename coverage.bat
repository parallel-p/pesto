@echo off
coverage.exe run testing_global.py
coverage.exe html -d coverage/
start coverage/index.html