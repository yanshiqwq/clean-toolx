@echo off
if "%1" == "/a" (goto :main)
net session>nul
if "%ERRORLEVEL%" NEQ "2" (
	goto :main
) else (
	mshta vbscript:CreateObject^("Shell.Application"^).ShellExecute^("cmd.exe","/c %~s0 /admin ::","","runas",1^)^(window.close^) & goto :eof)
)
:main
pushd %~dp0
python %~dp0\clean-toolx.py
pause