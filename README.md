# Qt Material UI

Material 3 component library for Qt Widgets

[![PyPI](https://img.shields.io/pypi/v/qt-material-ui.svg)](https://pypi.org/project/qt-material-ui/)
[![Docs](https://readthedocs.org/projects/qt-material-ui/badge/?version=latest)](https://qt-material-ui.readthedocs.io/en/latest/?badge=latest)
![License](https://img.shields.io/pypi/l/qt-material-ui.svg)
[![Tests](https://github.com/herobank110/qt-material-ui/actions/workflows/test.yml/badge.svg?branch=main)](https://github.com/herobank110/qt-material-ui/actions/workflows/test.yml)

## Get Started

This library is available on PyPI and can be installed with pip:

```bash
pip install qt-material-ui
```

For further information, check out the
[Get Started documentation](https://qt-material-ui.readthedocs.io/en/latest/get-started.html).

### Qt Version

This library has been tested with PySide 6.9.

## Development

### Documentation

The docs are kept in markdown format under the /docs directory. To
build the HTML, you should use [VitePress](https://vitepress.dev).
As a prerequisite, you will need NodeJS installed.

From the root of the repository, run the following command to install
vitepress:

```
npm install
```

Subsequently you can work on the docs with a hot reload server:

```
cd docs && npx vitepress
```

> This is also available as a VSCode task called `serve docs locally`.

#### Documentation Guidelines

Components should have a page which contains at least the following
elements: a brief description which may be copied from Material docs, a
gif showing it in action, a usage example, and API reference for props
and signals.

Other random pages may be added as needed but the components reference
is the most important.

Where possible markdown content should be wrapped at 72 characters.

## Contributing

Currently the library is in a very early stage but if you want to get
involved, feel free to reach out.
