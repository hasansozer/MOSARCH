# On the Use of Evolutionary Coupling for Software Architecture Recovery

Zip files include python code, `rsf` files, `jar` files and scripts that are used to generate the data in the article.
Outputs can also be found in them.
To try the code by yourself:

## Pre-requisites
1. Zip files: Download [Chromium](https://drive.google.com/file/d/1EViBzHzYE37mJrgA5h7XJC7fFt7S3KHb/view?usp=sharing), [Hadoop](https://drive.google.com/file/d/1muaxvF89LsrW6_2oap2UObLdB5Zy8g6n/view?usp=sharing), [ITK](https://drive.google.com/file/d/1muaxvF89LsrW6_2oap2UObLdB5Zy8g6n/view?usp=sharing) and extract all the files inside.
2. Download the git repos [Chromium](https://github.com/chromium/chromium), [Hadoop](https://github.com/apache/hadoop) and [ITK](https://github.com/InsightSoftwareConsortium/ITK) to a directory that has no read/write restrictions.
3. [Python](https://www.python.org/downloads/)
4. [Java](https://www.oracle.com/java/technologies/javase/javase-jdk8-downloads.html)
5. [PyDriller](https://github.com/ishepard/pydriller)
	* Use
	```
	pip install pydriller
	```
6. Scripts are in `.bat` format but can be transformed to `.sh` easily if you use a Linux system.

<br>

## For Hadoop & ITK
1. Open `main.py` and replace the line `repo = Repository('C:\\Users...')` with the path of the corresponding repository in your computer.
2. Run `main.py`. This will create the additional dependencies for each number of commits in `rsf` format.
3. Run `automaticacdc.py` and `automaticmcdc.py` to get the results from ACDC and MCDC clustering algorithms, respectively.

<br>

## Chromium
1. The commits are pre-downloaded to `2013-2012-clean.txt` because of git errors caused by `PyDriller`. You can replace the commit info inside `2013-2012-clean.txt` with another commit info in the same format.
2. Run `main.py`. This will create the additional dependencies for each number of commits in `rsf` format.
3. Run `automaticacdc.py` and `automaticmcdc.py` to get the results from ACDC and MCDC clustering algorithms, respectively.
