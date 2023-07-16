# Setting up
## Start by setting up your environment
```
$ . ./bootstrap
```
This will source you into an environment. You can safely do this any number of times, and you should do this whenever you open a new shell.

## Conventions
Run `pylint` on your files, make sure you get a 10.00/10 - this will be done as part of a pre-commit hook. Don't skip it. (Just run the pre-commit hooks and you'll be fine).

Aim for 85% or higher coverage. Test like this
```
$ coverage run --source='ecdh_signatures' -m behave
$ coverage report -m
```

## Running pre-commit checks manually
```
$ pre-commit run --all-files
```
## To build
```
python -m build
```
