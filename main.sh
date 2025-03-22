#!/bin/bash

cd `dirname "$0"`

pdm run python fill-cv-template.py

if [ $? -ne 0 ]
then
    echo "fill-cv-template.py failed, exiting"
    exit 1
fi

pdflatex cv.tex

pdm run python fill-cover-letter-template.py

if [ $? -ne 0 ]
then
    echo "fill-cover-letter-template.py failed, exiting"
    exit 1
fi

pdflatex cover-letter.tex
