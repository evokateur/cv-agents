#!/bin/bash

cd "$(dirname "$0")" || exit 1

if ! python fill-cv-template.py; then
    echo "fill-cv-template.py failed, exiting"
    exit 1
fi

if ! python fill-cover-letter-template.py; then
    echo "fill-cover-letter-template.py failed, exiting"
    exit 1
fi

if ! pdflatex cv.tex; then
    echo "pdflatex cv.tex failed, exiting"
    exit 1
fi

if ! pdflatex cover-letter.tex; then
    echo "pdflatex cover-letter.tex failed, exiting"
    exit 1
fi
