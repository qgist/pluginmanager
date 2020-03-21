# `/src/python/qgspythonutilsimpl.cpp`

This file does a lot of Python code injection, which can be removed (and be implemented in Python directly). Fetching relevant paths can be done in Python. Importing stuff and configuring `sip` can be done in Python.

What remains is controlling the Python interpreter, e.g. `Py_Initialize()` or `PyEval_InitThreads()`, and deactivating the Python integration in the event of a failure.
