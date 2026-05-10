@echo off
REM Build script for 三仙归洞 APK

cd /d "%~dp0"

set "JAVA_HOME=C:\Program Files\JetBrains\PyCharm Community Edition 2024.2.4\jbr"
set "PATH=%JAVA_HOME%\bin;C:\Program Files\Git\cmd;C:\Python314;%PATH%"

python -m buildozer android debug