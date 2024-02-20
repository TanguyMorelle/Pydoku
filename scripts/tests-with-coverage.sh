poetry run coverage run -m pytest -v
poetry run coverage report --fail-under=90
poetry run coverage html $@
