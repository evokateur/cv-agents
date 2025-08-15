#!/bin/bash

tree -I 'resources|vector_db|__pycache__|knowledge-base|__init__*|examples|*.aux|*.log|*.md|Makefile|data|output|*.sh|*.out|*.ipynb'|pbcopy
