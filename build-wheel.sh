#! /bin/bash
set -e
python3 -m venv .venv
. .venv/bin/activate
pip install -U pip
python3 -m build
