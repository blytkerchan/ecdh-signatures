#! /bin/bash
set -e
python3 -m venv .venv
. .venv/bin/activate
pip install -U pip build wheel
python3 -m build
