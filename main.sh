#!/bin/bash

cd `dirname "$0"`

python3 fill-cv-template.py
pdflatex cv.tex

python3 fill-cover-letter-template.py
pdflatex cover-letter.tex
