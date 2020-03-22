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

Information sources:

- `homePluginsPath()` returns a single path, `homePythonPath() + "/plugins"`, exposed in `qgis.utils.sys_plugin_path`.
- `pluginsPath()` returns a single path, `pythonPath() + "/plugins"`, exposed in `qgis.utils.home_plugin_path`.
- `extraPluginsPaths()` is parsing the `QGIS_PLUGINPATH` environment variable. Delimited by `:` on Unix, by `;` on Windows.

```C++
QString QgsPythonUtilsImpl::pythonPath() const
{
  if ( QgsApplication::isRunningFromBuildDir() )
    return QgsApplication::buildOutputPath() + QStringLiteral( "/python" );
  else
    return QgsApplication::pkgDataPath() + QStringLiteral( "/python" );
}

QString QgsPythonUtilsImpl::homePythonPath() const
{
  QString settingsDir = QgsApplication::qgisSettingsDirPath();
  if ( QDir::cleanPath( settingsDir ) == QDir::homePath() + QStringLiteral( "/.qgis3" ) )
  {
    return QStringLiteral( "\"%1/.qgis3/python\"" ).arg( QDir::homePath() );
  }
  else
  {
    return QStringLiteral( "\"" ) + settingsDir.replace( '\\', QLatin1String( "\\\\" ) ) + QStringLiteral( "python\"" );
  }
}
```

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

# Load / Reload / Unload - i.e. `import`

- https://stackoverflow.com/questions/4111640/how-to-reimport-module-to-python-then-code-be-changed-after-import
- https://stackoverflow.com/questions/437589/how-do-i-unload-reload-a-module
- `del`

LOAD != START

Load DOES NOT happen automatically on startup of QGIS. Only once (and if) the plugin is "activated". Plugin registry?

Loader traceback from crap test plugin:

```python
ValueError: YYY!
Traceback (most recent call last):
  File "$CONDA/envs/$ENV/share/qgis/python/qgis/utils.py", line 312, in loadPlugin
    __import__(packageName)
  File "$CONDA/envs/$ENV/share/qgis/python/qgis/utils.py", line 744, in _import
    mod = _builtin_import(name, globals, locals, fromlist, level)
  File "$HOME/.local/share/QGIS/QGIS3/profiles/$PROFILE/python/plugins/crap/__init__.py", line 3, in
    raise ValueError('YYY!')
ValueError: YYY!
```

There is an override in `utils.py`:

```python
if not os.environ.get('QGIS_NO_OVERRIDE_IMPORT'):
    if _uses_builtins:
        builtins.__import__ = _import
    else:
        __builtin__.__import__ = _import
```

# Init / unload - i.e. running the plugin and its GUI

Plugin class constructor traceback:

```python
Traceback (most recent call last):
  File "$CONDA/envs/$ENV/share/qgis/python/qgis/utils.py", line 334, in _startPlugin
    plugins[packageName] = package.classFactory(iface)
  File "$HOME/.local/share/QGIS/QGIS3/profiles/$PROFILE/python/plugins/crap/__init__.py", line 7, in classFactory
    return crap_plugin(iface)
  File "$HOME/.local/share/QGIS/QGIS3/profiles/$PROFILE/python/plugins/crap/__init__.py", line 12, in __init__
    raise ValueError('AAA!')
ValueError: AAA!
```

Plugin init GUI traceback:

```python
Traceback (most recent call last):
  File "$CONDA/envs/$ENV/share/qgis/python/qgis/utils.py", line 359, in startPlugin
    plugins[packageName].initGui()
  File "$HOME/.local/share/QGIS/QGIS3/profiles/$PROFILE/python/plugins/crap/__init__.py", line 14, in initGui
    raise ValueError('BBB!')
ValueError: BBB!
```

Plugin unload traceback:

```python
Traceback (most recent call last):
  File "$CONDA/envs/$ENV/share/qgis/python/qgis/utils.py", line 434, in unloadPlugin
    plugins[packageName].unload()
  File "$HOME/.local/share/QGIS/QGIS3/profiles/$PROFILE/python/plugins/crap/__init__.py", line 17, in unload
    raise ValueError('CCC!')
ValueError: CCC!
```

# UI / Qt

Plugin manager GUI uses `QgsScrollArea` and `QgsWebView`. The former, `QgsScrollArea`, is exposed as part of `qgis.gui`. The latter, `QgsWebView`, is not exposed. It is a wrapper around `QWebView`, see `/src/core/qgswebview.h`. If webkit is switched off at compile time, `QTextBrowser` is used instead.
