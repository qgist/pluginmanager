
# `def exportSettingsGroup(self)`

- called by C++
    - `QgsPluginManager::setPythonUtils`
    - `QgsPluginManager::reject`
    - `QgsPluginManager::ckbExperimental_toggled`
    - `QgsPluginManager::ckbDeprecated_toggled`

# `def onManagerClose(self)`

- called by C++
    - `QgsPluginManager::reject`

# `def sendVote(self, x, y)`

- called by C++
    - `QgsPluginManager::sendVote`

# `def upgradeAllUpgradeable(self)`

- called by C++
    - `QgsPluginManager::buttonUpgradeAll_clicked`

# `def installPlugin(self, x)`

- called by C++
    - `QgsPluginManager::buttonInstall_clicked`

# `def uninstallPlugin(self, x)`

- called by C++
    - `QgsPluginManager::buttonUninstall_clicked`

# `def installFromZipFile(self, x)`

- called by C++
    - `QgsPluginManager::buttonInstallFromZip_clicked`

# `def setRepositoryInspectionFilter(self, x)`

- called by C++
    - `QgsPluginManager::setRepositoryFilter`

# `def clearRepositoryFilter(self)`

- called by C++
    - `QgsPluginManager::clearRepositoryFilter`

# `def reloadAndExportData(self)`

- called by C++
    - `QgsPluginManager::buttonRefreshRepos_clicked`

# `def addRepository(self)`

- called by C++
    - `QgsPluginManager::buttonAddRep_clicked`

# `def editRepository(self, x)`

- called by C++
    - `QgsPluginManager::buttonEditRep_clicked`

# `def deleteRepository(self, x)`

- called by C++
    - `QgsPluginManager::buttonDeleteRep_clicked`

# `def exportPluginsToManager(self)`

- called by C++
    - `QgsPluginManager::ckbExperimental_toggled`
    - `QgsPluginManager::ckbDeprecated_toggled`
