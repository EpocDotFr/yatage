# YATAGE

<img align="right" src="https://raw.githubusercontent.com/EpocDotFr/yatage/master/docs/_static/logo_white.png">

Yet Another [Text Adventure Game](https://en.wikipedia.org/wiki/Interactive_fiction) Engine.

![Python versions](https://img.shields.io/pypi/pyversions/yatage.svg) ![Version](https://img.shields.io/pypi/v/yatage.svg) ![Tests](https://github.com/EpocDotFr/yatage/actions/workflows/tests.yml/badge.svg) ![License](https://img.shields.io/pypi/l/yatage.svg)

## Documentation

Everything you need to know is located [here](https://epocdotfr.github.io/yatage/).

## Development

### Getting source code and installing the package with dev dependencies

  1. Clone the repository
  2. From the root directory, run: `pip install -e .[dev]` on Linux or `pip install -e ".[dev]"` on Windows

### Running tests

From the root directory, run `pytest`. They will automatically be all discovered and ran.

> **Note** Tests are very basic ATM.

### Building docs

From the `docs` directory, run `make.bat html` on Windows or `make html` on Linux. Generated docs will be located in `docs/_build/html`.

### Releasing the package

From the root directory, run `python setup.py upload`. This will build the package, create a git tag and publish on PyPI.

`__version__` in `yatage/__version__.py` and `release` in `docs/conf.py` must be updated beforehand. These should adhere to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

An associated GitHub release must be created following the [Keep a Changelog](https://keepachangelog.com/en/1.0.0/) format.

## Credits

  - Logo by [Delapouite](https://game-icons.net/1x1/delapouite/dungeon-gate.html) ([CC BY 3.0](https://creativecommons.org/licenses/by/3.0/))
