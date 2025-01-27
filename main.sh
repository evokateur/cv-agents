#!/bin/bash

cd `dirname "$0"`

python3 fill-cv-template.py
pdflatex cv.tex

cp cover-letter-template.tex cover-letter.tex
pdflatex cover-letter.tex
