#!/usr/bin/env bash
set -e
python3 -m venv .venv
source .venv/bin/activate
pip install -U pip
pip install -r env/requirements.txt
echo "Build ok"
