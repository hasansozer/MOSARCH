@echo off

java -jar rsf2txt.jar %1 dep.txt

timer /n /q

java -jar clustering.jar dep.txt c.txt

timer /s /nologo

java -jar txt2rsf.jar c.txt c.rsf
java -jar mojo.jar c.rsf %2 -fm

rem Remove temporary files
del dep.txt
del c.txt
del c.rsf
