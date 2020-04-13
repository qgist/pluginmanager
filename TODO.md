
# Repository refresh

Currently, all repositories are refreshed when opening the plugin manager. There could be a cache and a "refresh interval option".

# Metadata (XML)

There are problems with "lonely ampersands".

```python
def _fix_metadata(metadata):
    "Fix lonely ampersands in metadata"

    a = _QByteArray()
    a.append("& ")
    b = _QByteArray()
    b.append("&amp; ")

    return metadata.replace(a, b)
```

# Metadata (TXT)

Are people using interpolation?

https://docs.python.org/3/library/configparser.html#configparser.BasicInterpolation

If activated, it is causing issues in some cases (e.g. `tuflow.3.0.4.zip`).

# Metadata - dependencies (QGIS legacy style)

Some folks use `plugin_dependencies` for Python package dependencies, e.g.

- go_to_xyz.0.2.zip: ('mercantile',)
- geodatafarm.2.6.0.zip: ('matplotlib', ' reportlab')

How should this be handled?

# Packaging

This plugin should not only be packaged as as QGIS plugin but also stand-alone as wheel and conda package. How does a reasonable project / directory structure look like?

# Testing

Use coverage (through [API](https://coverage.readthedocs.io/en/coverage-5.0.4/api_coverage.html)).

## `dtype_version_class`

- test run against plugin database while comparing against `python/pyplugin_installer/version_compare.py`
- fuzzing

Are commas valid version element delimiters?

# QGIS

How do I determine the version of QGIS by looking at the files in its installation folder (i.e. NOT by running QGIS and/or importing `qgis` in Python)?

How can I use images / resources from QGIS? Import them into source tree or attach to QGIS API?

# UI

Should the manager also work in CLI mode (for server use)?
