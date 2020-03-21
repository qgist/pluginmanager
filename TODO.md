
# Packaging

This plugin should not only be packaged as as QGIS plugin but also stand-alone as wheel and conda package. How does a reasonable project / directory structure look like?

# Testing

## `dtype_version_class`

- test run against plugin database while comparing against `python/pyplugin_installer/version_compare.py`
- fuzzing

Are commas valid version element delimiters?

# QGIS

How do I determine the version of QGIS by looking at the files in its installation folder (i.e. NOT by running QGIS and/or importing `qgis` in Python)?

How can I use images / resources from QGIS? Import them into source tree or attach to QGIS API?
