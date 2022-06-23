# Ping IP

## Setup

```shell
poetry install
```

## Run

### Method 1 (Recommended)

This method supports retry, skip list.

```shell
poetry run poe run-reactive
```

### Method 2

This method does not support retry, skip list.

Because no retry, so not reliable due to some IPs might get timeout in the first scan.

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
