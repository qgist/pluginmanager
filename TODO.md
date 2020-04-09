
# Repository refresh

Currently, all repositories are refreshed when opening the plugin manager. There could be a cache and a "refresh interval option".

# Auth

Qgis supports multiple methods of authentication (also for plugin download?). Access them through API and support for them in Qgis Legacy Python Plugins backend.

There is an authentication manager (with master password), which can somehow inject its data into a `QRequest`. Be aware that the Plugin Manager currently uses `requests` (Python package) for fetching data.

See:

- https://github.com/qgis/QGIS/blob/4e33bc1fcf76cf00c8288d16db3273bb05b43fea/src/auth/basic/qgsauthbasicmethod.cpp#L67
- https://github.com/qgis/QGIS/blob/c76c3904050ae3660ee42435380ae479958023bd/src/auth/oauth2/qgsauthoauth2method.cpp#L106

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
