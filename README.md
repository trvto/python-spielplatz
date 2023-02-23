# python-spielplatz

A python project to play around with modern software development concepts in python

## Installation

The python package is not currently hosted on PyPI. To install it, clone the repository
into a local directory and run

```
pip install -e <local_repository_root_dir>
```

## Local development

[poetry](https://python-poetry.org/), [nox](https://nox.thea.codes/en/stable/), and [pre-commit](https://pre-commit.com/) are used for dependency management, test automation and code quality checks.

### Suggested development setup

- Install [pyenv](https://github.com/pyenv/pyenv) to manage python versions according to documentation. (Not available on Windows, but there might be acceptable alternatives). E.g., with homebrew
  ```
  brew update
  brew install pyenv
  ```
  Follow instructions given during/after install.
  See documentation for usage.
- Install [pipx](https://github.com/pypa/pipx) (to install and run python applications in isolated environments):
  ```
  pip install pipx
  ```
- Install [poetry](https://python-poetry.org/) to manage project
  ```
  pipx install poetry
  ```
  - suggested poetry settings:
    - `poetry config virtualenvs.in-project true`
      - On `poetry install`, create virtual environment in current directory (instead of poetry's cache directory)
    - `poetry env use <python-version>`
      - Tell poetry to use the desired python version, e.g. `3.11`. If required version in pyproject.toml is higher than currently used version, poetry will complain
- Install [nox](https://nox.thea.codes/en/stable/) to perform automated development tasks
  ```
  pipx install nox
  ```
- Install [pre-commit](https://pre-commit.com/) to perform automated checks before each commit
  ```
  pipx install pre-commit
  ```
- Use [poetry](https://python-poetry.org/) to install project in an isolated virtual env
  From repository root
  ```
  poetry install
  ```

## Development tasks

### Nox

[nox](https://nox.thea.codes/en/stable/) is used for running a variety of development tasks (nox "sessions") through a
python script called `noxfile.py`.

List available sessions using `nox --list`. Run a session using `nox -s <session_name>`.
Per default, nox installs any dependencies for the session into a fresh virtual environment. To save time, pass the
`-r` flag to nox to reuse the last virtual env for that session.

Sessions:

- tests => run tests using [pytest](https://docs.pytest.org/en/7.2.x/), report test coverage using [coverage.py](https://coverage.readthedocs.io/en/7.1.0/)
- lint => code linting using [ruff](https://github.com/charliermarsh/ruff), reformatting using [black](https://github.com/psf/black), docstring checks with [darglint](https://pypi.org/project/darglint/)
- type_checking => static type checking using [mypy](https://mypy-lang.org/)
- docs => build documentation from docstrings using [sphinx](https://www.sphinx-doc.org/en/master/)
- safety => check dependencies for known vulnerabilities using [safety](https://pypi.org/project/safety/)

### Pre-Commit Hooks

When enabled, pre-commit hooks are checks that run whenever trying to commit to the repository. The checks make sure certain standards
and formats are upheld for the code. The checks that run are defined in the [.pre-commit-config.yaml](.pre-commit-config.yaml).

To enable pre-commit hooks, run (from the repository root):

```commandline
pre-commit install
```

In many cases, if the check fails, the files will be automatically reformatted to conform to the check.

# Modules

## Checkers

The checkers module contains a command line interface for playing the game of checkers. After installation with pip (or pipx),
the cli should be available und the command `checkers`.

To run within the development environment: after `poetry install`, use `poetry run checkers` to see cli documentation and `poetry run checkers <command>` to run
checkers commands.

<!-- github-only -->


This line is pointless
