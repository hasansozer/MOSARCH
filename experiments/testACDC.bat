@echo off

timer /n /q

java -jar acdc.jar %1 c.rsf

timer /s /nologo

java -jar mojo.jar c.rsf %2 -fm

rem Remove temporary files
del c.rsf




