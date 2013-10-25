@echo off
set PATH=%CD%;%PATH%;
java -jar -Djava.util.logging.config.file=logging.properties "%~dp0\apktool.jar" %1 %2 %3 %4 %5 %6 %7 %8 %9
