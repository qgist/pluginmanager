
# GLOBALS

- `iface`
    Interface
- `plugin_paths = []`
    list of plugin paths. it gets filled in by the QGIS python library
- `plugins = {}`
    dictionary of plugins
- `plugin_times = {}`
    ???
- `active_plugins = []`
    list of active (started) plugins
- `available_plugins = []`
    list of plugins in plugin directory and home plugin directory
- `plugins_metadata_parser = {}`
    dictionary of plugins providing metadata in a text file (metadata.txt)
    key = plugin package name, value = config parser instance

## `def findPlugins(path: str) -> GENERATOR`

- does
    - search with os module
    - "for internal use: return list of plugins in given path"
- yields
    - `(pluginName, cp)` # string, config parser

## `def metadataParser() -> dict`

- does
    - nothing
    - "Used by other modules to access the local parser object"
- GLOBALS
    - `plugins_metadata_parser` (no change)
- returns
    - `plugins_metadata_parser` (mutable, no copy)

## `def updateAvailablePlugins()`

- does
    - plugin search
    - "Go through the plugin_paths list and find out what plugins are available."
- GLOBALS
    - `available_plugins` (RE-ASSIGNMENT: list of names/strings)
    - `plugins_metadata_parser` (RE-ASSIGNMENT: dict of {name/string: config parser})
- calls
    - `findPlugins(pluginpath)`

## `def pluginMetadata(packageName: str, fct: str) -> str`

- does
    - fetch from package meta data field
    - "fetch metadata from a plugin - use values from metadata.txt"
- GLOBALS
    - `plugins_metadata_parser` (READ)
- returns
    - `plugins_metadata_parser[packageName].get('general', fct)` or `"__error__"`

## `def loadPlugin(packageName: str) -> bool`

- does
    - import (only)
    - "load plugin's package"
- calls
    - `__import__(packageName)`
- returns
    - `True`/`False` (success)

## `def _startPlugin(packageName: str) -> bool`

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

- does
    - "adds a plugin to the list of active plugins"
- GLOBALS
    - `active_plugins` (CHANGE: adding packageName)
    - `plugin_times` (CHANGE: adding/changing duration)

## `def startPlugin(packageName: str) -> bool`

- does
    - starts plugin GUI
    - "initialize the plugin"
- calls
    - `_startPlugin(packageName)`
    - `plugins[packageName].initGui()`
    - `_unloadPluginModules(packageName)` (if exception)
    - `_addToActivePlugins(packageName, end - start)`
- GLOBALS
    - `plugins` (READ: `plugins[packageName].initGui()` | WRITE: `del plugins[packageName]` if exception)
    - `active_plugins` (UNUSED)
    - `iface` (UNUSED)
    - `plugin_times` (UNUSED)
- returns
    - `True`/`False` (success)

## `def startProcessingPlugin(packageName: str) -> bool`

- does
    - starts plugin processing
    - "initialize only the Processing components of a plugin"
- calls
    - `_startPlugin(packageName)`
    - `_unloadPluginModules(packageName)` (if exception or `initProcessing` not present)
    - `plugins[packageName].initProcessing()`
    - `_addToActivePlugins(packageName, end - start)`
- GLOBALS
    - `plugins` (READ: `plugins[packageName].initProcessing()` | WRITE: `del plugins[packageName]` if exception)
    - `active_plugins` (UNUSED)
    - `iface` (UNUSED)
    - `plugin_times` (UNUSED)
- returns
    - `True`/`False` (success)

## `def canUninstallPlugin(packageName: str) -> bool`

- does
    - Check if
        - plugin is active (`active_plugins`)
        - plugin in in `plugins` (results of `classFactory`)
    - "confirm that the plugin can be uninstalled"
- calls
    - `plugins[packageName].canBeUninstalled()` if `canBeUninstalled` is present
- GLOBALS
    - `plugins` (READ)
    - `active_plugins` (READ)
- returns
    - `True`/`False` (yes/no)

## `def unloadPlugin(packageName: str) -> bool`

- does
    - try/except around actual unload function
    - "unload and delete plugin!"
- calls
    - `plugins[packageName].unload()` (plugin GUI unload API)
    - `_unloadPluginModules(packageName)`
- GLOBALS
    - `plugins` (WRITE: `del plugins[packageName]`)
    - `active_plugins` (WRITE: `active_plugins.remove(packageName)`)
- returns
    - `True`/`False` (success)

## `def _unloadPluginModules(packageName: str)`

- does
    - Qt resources cleanups
    - Deleting entries in `sys.modules` (dict)
    - "unload plugin package with all its modules (files)"
- calls
    - `sys.modules[mod].qCleanupResources()` (for mod in `_plugin_modules[packageName]`) if present
- GLOBALS
    - `_plugin_modules` (WRITE: `del _plugin_modules[packageName]`)

## `def isPluginLoaded(packageName: str) -> bool`

- does
    - check if plugin is present in dict
    - "find out whether a plugin is active (i.e. has been started)"
- GLOBALS
    - `plugins` (READ)
    - `active_plugins` (READ)
- returns
    - `True`/`False` (yes/no)

## `def reloadPlugin(packageName: str)`

- does
    - "unload and start again a plugin"
- calls
    - `unloadPlugin(packageName)`
    - `loadPlugin(packageName)`
    - `startPlugin(packageName)`
- GLOBALS
    - `active_plugins` (READ)

## `def showPluginHelp(packageName = None: str, filename="index": str, section="": str)`

- does
     - locates a localized help (index), opens it in browser
     - "show a help in the user's html browser. The help file should be named index-ll_CC.html or index-ll.html"

## `def pluginDirectory(packageName: str) -> str`

- does
    - locates plugin root directory (for one plugin)
    - "return directory where the plugin resides. Plugin must be loaded already"
- returns
    - path (to plugin module root directory)

<!-- MACROS -->

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
