#!/bin/bash

tree -I 'pytest.ini|requirements.txt|sample.env|tests|_docs|job_postings|vector_db|__pycache__|knowledge-base|__init__*|examples|*.aux|*.log|*.md|Makefile|output|*.sh|*.out|*.ipynb|*.lock|scripts' | sed '$d; $d' | tee >(pbcopy)

echo "(copied to paste buffer)"
