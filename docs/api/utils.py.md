
# BLOCK 1

## GLOBALS

- `iface`
    - Interface
    - ASSIGNMENT: `initInterface()`
- `plugin_paths = []`
    - list of plugin paths
    - ASSIGNMENT (C++): `QgsPythonUtilsImpl::checkSystemImports`
    - READ: `installer_data.Pluginsget.AllInstalled()`
- `plugins = {}` (**NONE**)
    - dictionary of plugins
    - WRITE: `_startPlugin()`
    - WRITE: `startPlugin()`
    - WRITE: `startProcessingPlugin()`
    - READ: `canUninstallPlugin()`
    - WRITE: `unloadPlugin()`
    - READ: `isPluginLoaded()`
- `plugin_times = {}` (**NONE**)
    - WRITE: `_addToActivePlugins()`
- `active_plugins = []` (**WRAP**)
    - list of active (started) plugins
    - READ: `QgsPythonUtilsImpl::listActivePlugins()` in `'\n'.join(qgis.utils.active_plugins)`
    - READ: `_startPlugin()`
    - WRITE: `_addToActivePlugins()`
    - READ: `canUninstallPlugin()`
    - WRITE: `unloadPlugin()`
    - READ: `isPluginLoaded()`
    - READ: `reloadPlugin()`
- `available_plugins = []` (**WRAP**)
    - list of plugins in plugin directory and home plugin directory
    - READ (C++): `QgsPythonUtilsImpl::pluginList()` in `'\n'.join(qgis.utils.available_plugins)`
    - ASSIGNMENT: `updateAvailablePlugins()`
- `_plugin_modules = {}` (**NONE**)
    - dict of imported (plugin) modules
    - WRITE: `builtins.__import__`
    - WRITE: `_unloadPluginModules()`

- `plugins_metadata_parser = {}` (**WRAP**)
    - dictionary of plugins providing metadata in a text file (metadata.txt)
    - key = plugin package name : value = config parser instance
    - WRITE: `installer.pluginInstaller.uninstallPlugin()` (`del` key/value pair)
    - READ: `metadataParser()` and passes it on via return!
    - ASSIGNMENT: `updateAvailablePlugins()`
    - READ: `pluginMetadata()`

Variables created by `qgspythonutilsimpl.cpp`:

- `sys_plugin_path`
- `home_plugin_path`
    - READ: `installer.pluginInstaller.installPlugin()`
    - READ: `installer.pluginInstaller.uninstallPlugin()`
    - READ: `installer.pluginInstaller.installFromZipFile()`
    - READ: `installer_data.removeDir()`

## `def initInterface(pointer: int)`

- does
    - creates `iface` object
- GLOBALS
    - `iface` (ASSIGNMENT)

## `def findPlugins(path: str) -> GENERATOR`

**NO_IMPLEMENTATION**

- does
    - search with os module
    - "for internal use: return list of plugins in given path"
- yields
    - `(pluginName, cp)` # string, config parser

## `def metadataParser() -> dict`

Only used in `plugindependencies.py`.

- does
    - nothing
    - "Used by other modules to access the local parser object"
- GLOBALS
    - `plugins_metadata_parser` (no change)
- returns
    - `plugins_metadata_parser` (mutable, no copy)

## `def updateAvailablePlugins()`

**RE_IMPLEMENTATION**

- does
    - plugin search
    - "Go through the plugin_paths list and find out what plugins are available."
- GLOBALS
    - `available_plugins` (RE-ASSIGNMENT: list of names/strings)
    - `plugins_metadata_parser` (RE-ASSIGNMENT: dict of {name/string: config parser})
- calls
    - `findPlugins(pluginpath)`
- called by C++
    - `QgsPythonUtilsImpl::pluginList()`
- called by Python
    - `installer.pluginInstaller.__init__`
    - `installer.pluginInstaller.installPlugin`
    - `installer.pluginInstaller.installFromZipFile`

## `def pluginMetadata(packageName: str, fct: str) -> str`

**RE_IMPLEMENTATION**

- does
    - fetch from package meta data field
    - "fetch metadata from a plugin - use values from metadata.txt"
- GLOBALS
    - `plugins_metadata_parser` (READ)
- called by C++
    - `QgsPythonUtilsImpl::getPluginMetadata`
- returns
    - `plugins_metadata_parser[packageName].get('general', fct)` or `"__error__"`

## `def loadPlugin(packageName: str) -> bool`

**RE_IMPLEMENTATION**

- does
    - import (only)
    - "load plugin's package"
- calls
    - `__import__(packageName)`
- called by C++
    - `QgsPythonUtilsImpl::loadPlugin`
- called by Python
    - `installer.pluginInstaller.__init__`
    - `installer.pluginInstaller.installPlugin`
    - `installer.pluginInstaller.installFromZipFile`
- returns
    - `True`/`False` (success)

## `def _startPlugin(packageName: str) -> bool`

**NO_IMPLEMENTATION**

- does
    - load plugin by calling its `classFactory` (i.e. regular plugins, not server)
    - "initializes a plugin, but does not load GUI"
- calls
    - `sys.modules[packageName].classFactory(iface)`
    - `_unloadPluginModules(packageName)` (only if above raises an exception)
- GLOBALS
    - `plugins` (CHANGE: adding {packageName: classFactory(iface)})
    - `active_plugins` (READ)
    - `iface` (READ: sent to classFactory)
    - `plugin_times` (UNUSED)
- returns
    - `True`/`False` (success)

## `def _addToActivePlugins(packageName: str, duration: float)`

**NO_IMPLEMENTATION**

- does
    - "adds a plugin to the list of active plugins"
- GLOBALS
    - `active_plugins` (CHANGE: adding packageName)
    - `plugin_times` (CHANGE: adding/changing duration)

## `def startPlugin(packageName: str) -> bool`

**RE_IMPLEMENTATION**

- does
    - starts plugin GUI
    - "initialize the plugin"
- calls
    - `_startPlugin(packageName)`
    - `plugins[packageName].initGui()`
    - `_unloadPluginModules(packageName)` (if exception)
    - `_addToActivePlugins(packageName, end - start)`
- called by C++
    - `QgsPythonUtilsImpl::startPlugin`
- called by Python
    - `installer.pluginInstaller.__init__`
    - `installer.pluginInstaller.installPlugin`
    - `installer.pluginInstaller.installFromZipFile`
- GLOBALS
    - `plugins` (READ: `plugins[packageName].initGui()` | WRITE: `del plugins[packageName]` if exception)
    - `active_plugins` (UNUSED)
    - `iface` (UNUSED)
    - `plugin_times` (UNUSED)
- returns
    - `True`/`False` (success)

## `def startProcessingPlugin(packageName: str) -> bool`

**RE_IMPLEMENTATION**

- does
    - starts plugin processing
    - "initialize only the Processing components of a plugin"
- calls
    - `_startPlugin(packageName)`
    - `_unloadPluginModules(packageName)` (if exception or `initProcessing` not present)
    - `plugins[packageName].initProcessing()`
    - `_addToActivePlugins(packageName, end - start)`
- called by C++
    - `QgsPythonUtilsImpl::startProcessingPlugin`
- GLOBALS
    - `plugins` (READ: `plugins[packageName].initProcessing()` | WRITE: `del plugins[packageName]` if exception)
    - `active_plugins` (UNUSED)
    - `iface` (UNUSED)
    - `plugin_times` (UNUSED)
- returns
    - `True`/`False` (success)

## `def canUninstallPlugin(packageName: str) -> bool`

**RE_IMPLEMENTATION**

- does
    - Check if
        - plugin is active (`active_plugins`)
        - plugin in in `plugins` (results of `classFactory`)
    - "confirm that the plugin can be uninstalled"
- calls
    - `plugins[packageName].canBeUninstalled()` if `canBeUninstalled` is present
- called by C++
    - `QgsPythonUtilsImpl::canUninstallPlugin`
- GLOBALS
    - `plugins` (READ)
    - `active_plugins` (READ)
- returns
    - `True`/`False` (yes/no)

## `def unloadPlugin(packageName: str) -> bool`

**RE_IMPLEMENTATION**

- does
    - try/except around actual unload function
    - "unload and delete plugin!"
- calls
    - `plugins[packageName].unload()` (plugin GUI unload API)
    - `_unloadPluginModules(packageName)`
- called by C++
    - `QgsPythonUtilsImpl::unloadPlugin`
- called by Python
    - `installer.pluginInstaller.installPlugin`
    - `installer.pluginInstaller.uninstallPlugin`
    - `installer.pluginInstaller.installFromZipFile`
- GLOBALS
    - `plugins` (WRITE: `del plugins[packageName]`)
    - `active_plugins` (WRITE: `active_plugins.remove(packageName)`)
- returns
    - `True`/`False` (success)

## `def _unloadPluginModules(packageName: str)`

**NO_IMPLEMENTATION**

- does
    - Qt resources cleanups
    - Deleting entries in `sys.modules` (dict)
    - "unload plugin package with all its modules (files)"
- calls
    - `sys.modules[mod].qCleanupResources()` (for mod in `_plugin_modules[packageName]`) if present
- GLOBALS
    - `_plugin_modules` (WRITE: `del _plugin_modules[packageName]`)

## `def isPluginLoaded(packageName: str) -> bool`

**RE_IMPLEMENTATION**

- does
    - check if plugin is present in dict
    - "find out whether a plugin is active (i.e. has been started)"
- called by C++
    - `QgsPythonUtilsImpl::isPluginLoaded`
- GLOBALS
    - `plugins` (READ)
    - `active_plugins` (READ)
- returns
    - `True`/`False` (yes/no)

## `def reloadPlugin(packageName: str)`

**RE_IMPLEMENTATION**

- does
    - "unload and start again a plugin"
- calls
    - `unloadPlugin(packageName)`
    - `loadPlugin(packageName)`
    - `startPlugin(packageName)`
- called by Python
    - `installer.pluginInstaller.installPlugin`
    - `installer.pluginInstaller.installFromZipFile`
- GLOBALS
    - `active_plugins` (READ)

## `def showPluginHelp(packageName = None: str, filename="index": str, section="": str)`

- does
     - locates a localized help (index), opens it in browser
     - "show a help in the user's html browser. The help file should be named index-ll_CC.html or index-ll.html"

## `def pluginDirectory(packageName: str) -> str`

**RE_IMPLEMENTATION**

- does
    - locates plugin root directory (for one plugin)
    - "return directory where the plugin resides. Plugin must be loaded already"
- returns
    - path (to plugin module root directory)

# BLOCK 2

## `def reloadProjectMacros()`

- does
    - no description, does not look like it's plugin related
- calls
    - `unloadProjectMacros()`
    - `QgsProject.instance().readEntry("Macros", "/pythonCode")`
    - `openProjectMacro()`

## `def unloadProjectMacros()`

- does
    - no description, does not look like it's plugin related
- calls
    - `closeProjectMacro()`

## `def openProjectMacro()`

- does
    - no description, does not look like it's plugin related

## `def saveProjectMacro()`

- does
    - no description, does not look like it's plugin related

## `def closeProjectMacro()`

- does
    - no description, does not look like it's plugin related

# BLOCK 3

## GLOBALS

- `server_plugin_paths = []`
    - list of plugin paths. Never filled ...
    - UNUSED
- `server_plugins = {}`
    - dictionary of plugins
    - WRITE: `startServerPlugin()`
- `server_active_plugins = []`
    - Interface
    - WRITE: `startServerPlugin()`
- `serverIface = None`
    - initialize 'serverIface' object
    - ASSIGNMENT: `initServerInterface()`

## `def initServerInterface(pointer: int)`

- does
    - creates `serverIface` object
- GLOBALS
    - `serverIface` (ASSIGNMENT)

## `def startServerPlugin(packageName: str) -> bool`

**RE_IMPLEMENTATION**

- does
    - triggers a plugin's `serverClassFactory` (if plugin is imported)
    - "initialize the plugin"
- calls
    - `sys.modules[packageName].serverClassFactory(serverIface)`
    - `_unloadPluginModules(packageName)` (if exception)
- GLOBALS
    - `server_plugins` (WRITE: `server_plugins[packageName] = sys.modules[packageName].serverClassFactory(serverIface)`)
    - `server_active_plugins` (WRITE: `server_active_plugins.append(packageName)`)
    - `serverIface` (READ)
- returns
    - `True`/`False` (success)
