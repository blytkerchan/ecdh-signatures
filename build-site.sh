#! /bin/bash
python3 -m venv .venv
. .venv/bin/activate
pip install -U pip
pip install -Ur paper-requirements.txt
jupyter nbconvert --ClearOutputPreprocessor.enabled=True --inplace paper.ipynb
jupyter nbconvert --execute --to notebook --inplace paper.ipynb
jupyter nbconvert paper.ipynb --to html --template classic --output-dir _site --output index
ghp-import -n -p -f _site
jupyter nbconvert --ClearOutputPreprocessor.enabled=True --inplace paper.ipynb
