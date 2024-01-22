# PyArticles
A LaTeX alternative that uses Python classes to output a HTML + CSS file that can be printed

To use this program, you must first create a conda environment (only 3.12 tested) and install all requirements.txt

Then, you must launch the Django server using the command in 'run.sh'

To visuallize your documents, you must go to the URL Django was launched to (default: http://localhost:8000)

To edit the documents, you can go to /Documents/generated/*/generate.py<br/>
This file contains the instructions (as Python classes & functions) to generate the output document

To print the document, you must go to your preferred browser and print it from there.<br/>
The document will contain special CSS to format the output PDF.
