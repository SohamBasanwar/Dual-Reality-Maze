@echo off
setlocal
set "maze_node="
for /f "delims=" %%N in ('where node.exe 2^>nul') do if not defined maze_node set "maze_node=%%N"
if not defined maze_node if exist "%ProgramFiles%\nodejs\node.exe" set "maze_node=%ProgramFiles%\nodejs\node.exe"
if not defined maze_node (
 echo Node.js is required. Install the LTS version from https://nodejs.org and try again.
 pause
 exit /b 1
)
"%maze_node%" "%~dp0launch.mjs" %*
if errorlevel 1 (
 pause
 exit /b 1
)
exit /b 0
