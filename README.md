# Ping IP

## Setup

```shell
poetry install
```

## Run

### Method 1 (Better)

This method supports retry, skip list. It leverages the power of [RxPY](https://github.com/ReactiveX/RxPY).

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

It uses [Mypy](https://github.com/python/mypy) to static type check the code.

```shell
poetry run poe static-type-check-mypy
```

## Lint

It uses [Black](https://github.com/psf/black), [Flake8](https://github.com/PyCQA/flake8), [isort](https://github.com/PyCQA/isort) to lint the code.

```shell
poetry run poe lint-black
poetry run poe lint-black-fix
poetry run poe lint-flake8
poetry run poe lint-isort
poetry run poe lint-isort-fix
```

## Test

This includes unit testing and [marble testing](https://rxjs.dev/guide/testing/marble-testing).

```shell
poetry run poe test
```
