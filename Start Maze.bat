@echo off
setlocal
call "%~dp0hardware\arduino-system\Start Hardware Game.bat" %*
exit /b %errorlevel%
