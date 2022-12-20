# YATAGE

Yet Another [Text Adventure Game](https://en.wikipedia.org/wiki/Interactive_fiction) Engine.

![Python versions](https://img.shields.io/pypi/pyversions/yatage.svg) ![Version](https://img.shields.io/pypi/v/yatage.svg) ![License](https://img.shields.io/pypi/l/yatage.svg)

## Documentation

Everything you need to know is located [here](https://epocdotfr.github.io/yatage/).

## Changelog

See [here](https://github.com/EpocDotFr/yatage/releases).

## Development

**Getting source code, installing the package as well as its dev packages:**

  1. Clone the repository
  2. From the root directory, run: `pip install -e .[dev]` on Linux or `pip install -e ".[dev]"` on Windows

**Building docs:**

From the `docs` directory, run `make.bat html` on Windows or `make html` on Linux.

**Publishing the package:**

From the root directory, run `python setup.py upload`. This will create a git tag and publish on PyPI.