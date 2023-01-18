# YATAGE

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="/docs/_static/logo_white.png">
  <source media="(prefers-color-scheme: light)" srcset="/docs/_static/logo_transparent.png">
  <img src="/docs/_static/logo_white.png" align="right">
</picture>

Yet Another [Text Adventure Game](https://en.wikipedia.org/wiki/Interactive_fiction) Engine.

![Python versions](https://img.shields.io/pypi/pyversions/yatage.svg) ![Version](https://img.shields.io/pypi/v/yatage.svg) ![License](https://img.shields.io/pypi/l/yatage.svg)

## Documentation

Everything you need to know is located [here](https://epocdotfr.github.io/yatage/).

## Development

**Getting source code, installing the package as well as its dev dependencies:**

  1. Clone the repository
  2. From the root directory, run: `pip install -e .[dev]` on Linux or `pip install -e ".[dev]"` on Windows

**Building docs:**

From the `docs` directory, run `make.bat html` on Windows or `make html` on Linux. Generated docs will be located in `docs/_build/html`.

**Publishing the package:**

From the root directory, run `python setup.py upload`. This will build the package, create a git tag and publish on PyPI.

`VERSION` in `setup.py` must be updated beforehand.

## Credits

  - Logo by [Delapouite](https://game-icons.net/1x1/delapouite/dungeon-gate.html) ([CC BY 3.0](https://creativecommons.org/licenses/by/3.0/))
