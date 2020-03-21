# Original QGIS Plugin Manager

(The following notes are based on an e-mail sent to the QGIS developer mailing list.)

It is an interesting mix of C++ and Python code. Even the plugin management GUI itself is partially C++ (the main window,
`QgsPluginManager[Interface]`, and part of its logic) and partially Python (all further dialogs and their logic).

Underneath `/python/pyplugin_installer/`, The class `QgsPluginInstaller` from `installer.py` appears to be a Python API that is called from the C++-interface (`QgsPluginManagerInterface`) through `QgsPythonRunner`. Most of the C++ appears to be located underneath `/src/app/pluginmanager/` (with a single ui-file elsewhere, `/src/ui/qgspluginmanagerbase.ui`). Having analyzed the C++ class `QgsPluginManager` I believe most of the interface can easily ported to Python.

`/src/app/qgspluginregistry.cpp` offers a class named `QgsPluginRegistry` (which is being used by `QgsPluginManager`). I have not found a way to access this class (or an/the instance of it) from Python. I figure it is required to handle both Python *and* C++ plugins. `QgsPluginRegistry` makes heavy use of `mPythonUtils`, which appears to be a C++ wrapper around `/python/utils.py` (through `/src/python/qgspythonutilsimpl.cpp`). So this portion of `QgsPluginRegistry` (about 50%) can be rewritten in Python rather quickly. Methods such as `loadCppPlugin` or `unloadCppPlugin` are a lot more problematic. As far as I can tell, those would need to remain in C++ and they would need to be exposed to Python somehow (if they are not already).

# `plugin_paths` (in C++ named `pluginpaths`)

Populated in `/src/python/qgspythonutilsimpl.cpp`, `QgsPythonUtilsImpl::checkSystemImports()`.

```C++
QStringList pluginpaths;
Q_FOREACH ( QString p, extraPluginsPaths() ) {
  pluginpaths << '"' + p + '"';
}
pluginpaths << homePluginsPath();
pluginpaths << '"' + pluginsPath() + '"';
runString( QStringLiteral( "qgis.utils.plugin_paths = [%1]" ).arg( pluginpaths.join( ',' ) ) );
```

Exposed as `qgis.utils.plugin_paths`. On conda:

- $HOME/.local/share/QGIS/QGIS3/profiles/$PROFILE/python/plugins (`home_plugin_path`)
- $CONDA/envs/$ENV/share/qgis/python/plugins (`sys_plugin_path`)

`homePluginsPath()` returns a single path, exposed in `qgis.utils.sys_plugin_path`.
`pluginsPath()` returns a single path, exposed in `qgis.utils.home_plugin_path`.

# `sys.path`

Populated in `/src/python/qgspythonutilsimpl.cpp`, `QgsPythonUtilsImpl::checkSystemImports()`.

```C++
newpaths << '"' + pythonPath() + '"';
newpaths << homePythonPath();
newpaths << pluginpaths;
runString( "sys.path = [" + newpaths.join( QStringLiteral( "," ) ) + "] + sys.path" );
```

On conda, in the following order, including all duplicate entries:

- $CONDA/envs/$ENV/share/qgis/python
- $HOME/.local/share/QGIS/QGIS3/profiles/$PROFILE/python
- $HOME/.local/share/QGIS/QGIS3/profiles/$PROFILE/python/plugins
- $CONDA/envs/$ENV/share/qgis/python/plugins
- $CONDA/envs/$ENV/share/qgis/python/plugins
- $CONDA/envs/$ENV/share/qgis/python
- $PWD
- $CONDA/envs/$ENV/lib/python37.zip
- $CONDA/envs/$ENV/lib/python3.7
- $CONDA/envs/$ENV/lib/python3.7/lib-dynload
- $HOME/.local/lib/python3.7/site-packages
- $CONDA/envs/$ENV/lib/python3.7/site-packages
- $HOME/.local/share/QGIS/QGIS3/profiles/$PROFILE/python
