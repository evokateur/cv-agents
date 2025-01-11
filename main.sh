#!/bin/bash

cd `dirname "$0"`

python3 fill-template.py
pdflatex cv.tex
