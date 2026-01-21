@echo off
REM Jatti Language - Windows Command Line Wrapper
REM Usage: jatti run file.jatti
REM        jatti build file.jatti -o output.py
REM        jatti format file.jatti -i

cd /d "%~dp0"
python cli.py %*
