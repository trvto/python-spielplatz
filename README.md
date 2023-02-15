# python-spielplatz
A python project to play around with modern software development concepts

## Suggested poetry settings
 - `poetry config virtualenvs.in-project true`
   - On `poetry install`, create virtual environment in current directory (instead of poetry's cache directory)
 - `poetry env use <python-version>`
   - Tell poetry to use the desired python version, e.g. `3.11`. If required version in pyproject.toml is higher than currently used version, poetry will complain