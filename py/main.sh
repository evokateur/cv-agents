#!/bin/bash

cd `dirname "$0"`

python3 script.py
pdflatex resume.tex
