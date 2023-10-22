build:
	python -m build

test:
	python -m pytest

publish:
	twine upload --skip-existing dist/*