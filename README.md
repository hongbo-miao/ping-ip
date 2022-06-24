# Ping IP

## Setup

```shell
poetry install
```

## Run

### Method 1 (Better)

This method supports retry, skip list.

You can change the config by updating the `reactive/config.py` file.

The code is in the `reactive` folder.

```shell
poetry run poe run-reactive
```

### Method 2

This method does not support retry, skip list.

Since there is no retry, it is not reliable because the only scan can get timeout.

The code is in the `multiprocess` folder.

```shell
poetry run poe run-multiprocess
```

## Static Type Check

```shell
poetry run poe static-type-check-mypy
```

## Lint

```shell
poetry run poe lint-black
poetry run poe lint-black-fix
poetry run poe lint-flake8
poetry run poe lint-isort
poetry run poe lint-isort-fix
```

## Test

```shell
poetry run poe test
```
