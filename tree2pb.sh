#!/bin/bash

tree -I '_docs|vector_db|__pycache__|knowledge-base|__init__*|examples|*.aux|*.log|*.md|Makefile|data|output|*.sh|*.out|*.ipynb' | sed '$d; $d' | tee >(pbcopy)

echo "(copied to paste buffer)"
