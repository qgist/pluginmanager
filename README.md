# QGIST Plugin Manager

## Synopsis

QGIST Plugin Manager is a QGIS plugin for managing QGIS plugins.
It is part of a larger effort, the [QGIST project](http://www.qgist.org).

This project attempts to replace QGIS' original plugin manager.

**ATTENTION: THIS PROJECT IS PRE-ALPHA! DO NOT USE!**

## How to test

There is no working graphical user interface yet **but** the plugin manager can be tested from the Python Console. Once this plugin is installed, the plugin index is exposed as `iface.pindex`. Go from there.

## For developers (how to contribute)

This is a CPython 3.6+ project. Keep exposure to PyQt and QGIS APIs to a minimum, i.e. Python standard library first wherever possible and strict conversions of (Py)Qt data types to Python data types. For now, no Python (or other) dependencies. PyQt is assumed to be importable, but the code should run without QGIS importable wherever possible. Type hints are considered, possibly enforced by [typeguard](https://github.com/agronholm/typeguard), but for now every API does "manual" type and bounds checks on all parameters.

Exceptions (i.e. current dependencies beyond PyQt):

- xmltodict

## Screenshots

None (yet).

## Branches

* `master`: More or less **stable**, contains latest **release**.
* `develop`: Latest (merged) developments, likely **unstable**. Please issue pull requests against this branch.
