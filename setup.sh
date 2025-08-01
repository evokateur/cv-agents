#!/bin/bash

python -m venv .venv --clear
source .venv/bin/activate
pip install -r requirements.txt
python -m ipykernel install --user --name=cv-agent --display-name "CV Agent"
