# Original QGIS Plugin Manager

(The following notes are based on an e-mail sent to the QGIS developer mailing list.)

It is an interesting mix of C++ and Python code. Even the plugin management GUI itself is partially C++ (the main window,
`QgsPluginManager[Interface]`, and part of its logic) and partially Python (all further dialogs and their logic).

Underneath `/python/pyplugin_installer/`, The class `QgsPluginInstaller` from `installer.py` appears to be a Python API that is called from the C++-interface (`QgsPluginManagerInterface`) through `QgsPythonRunner`. Most of the C++ appears to be located underneath `/src/app/pluginmanager/` (with a single ui-file elsewhere, `/src/ui/qgspluginmanagerbase.ui`). Having analyzed the C++ class `QgsPluginManager` I believe most of the interface can easily ported to Python.

`/src/app/qgspluginregistry.cpp` offers a class named `QgsPluginRegistry` (which is being used by `QgsPluginManager`). I have not found a way to access this class (or an/the instance of it) from Python. I figure it is required to handle both Python *and* C++ plugins. `QgsPluginRegistry` makes heavy use of `mPythonUtils`, which appears to be a C++ wrapper around `/python/utils.py` (through `/src/python/qgspythonutilsimpl.cpp`). So this portion of `QgsPluginRegistry` (about 50%) can be rewritten in Python rather quickly. Methods such as `loadCppPlugin` or `unloadCppPlugin` are a lot more problematic. As far as I can tell, those would need to remain in C++ and they would need to be exposed to Python somehow (if they are not already).
