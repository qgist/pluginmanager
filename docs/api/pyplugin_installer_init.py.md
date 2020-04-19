
# GLOBALS / EXPOSING

- `pyplugin_installer.installer` as `installer`
- `pyplugin_installer.installer.initPluginInstaller` as `initPluginInstaller`

# `def instance()`

- called by C++
    - `QgsPluginManager::setPythonUtils`
- returns
    - `pyplugin_installer.installer.pluginInstaller` (the one and instance: `pluginInstaller = QgsPluginInstaller()`)
