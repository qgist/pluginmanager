# `/src/python/qgspythonutilsimpl.cpp`

This file does a lot of Python code injection, which can be removed (and be implemented in Python directly). Fetching relevant paths can be done in Python. Importing stuff and configuring `sip` can be done in Python.

What remains is controlling the Python interpreter, e.g. `Py_Initialize()` or `PyEval_InitThreads()`, and deactivating the Python integration in the event of a failure.

# `/tests/src/app/testqgisapppython.cpp`

Remove tests for unnecessary C++ code, move test of relevant Python code to Python.

# `/python/utils.py`

Still contains highly critical Python 2 compatibility code (which is not marked in any way, shape or form). Must be removed. See [commit](https://github.com/qgis/QGIS/commit/02c56371555675aad012a903f9c8d79e913a9c5c) and [commit](https://github.com/qgis/QGIS/commit/2d3b813d227ca5d87690dd9eca1164c48dae594a). There is probably more (not yet identified).

# `/src/app/qgspluginregistry.cpp`

Is `QgsPluginRegistry::restoreSessionPlugins` being used at all? Search shots now result ...
