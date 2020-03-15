# -*- coding: utf-8 -*-

"""

QGIST PLUGIN MANAGER
QGIS Plugin for Managing QGIS Plugins
https://github.com/qgist/pluginmanager

    qgist/pluginmanager/dtype_plugin.py: Plugin data type

    Copyright (C) 2017-2020 QGIST project <info@qgist.org>

<LICENSE_BLOCK>
The contents of this file are subject to the GNU General Public License
Version 2 ("GPL" or "License"). You may not use this file except in
compliance with the License. You may obtain a copy of the License at
https://www.gnu.org/licenses/old-licenses/gpl-2.0.txt
https://github.com/qgist/pluginmanager/blob/master/LICENSE

Software distributed under the License is distributed on an "AS IS" basis,
WITHOUT WARRANTY OF ANY KIND, either express or implied. See the License for the
specific language governing rights and limitations under the License.
</LICENSE_BLOCK>

"""

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# CLASS
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

class dtype_plugin_class:
    """
    # One single plugin

    This is abstract class representing a plugin.
    From this, classes for plugin types (i.e. plugin sources) are derived?
    Or use repo type classes instead instead of having multiple plugin classes?

    - Dependencies:
        - inter-plugin
        - plugin to python packages (through source / other package manager)
    - Properties:
        - NAME / ID
        - Active
        - Installed
        - Installed version
        - Available versions (from sources ...)
        - upgradable
        - downgradable
        - orphan
        - meta ...
        - Caches
        - SETTINGS
    """

    def install(self):
        """
        Allows dry runs
        """
        pass
    def uninstall(self):
        """
        Allows dry runs
        """
        pass
    def upgrade(self, version):
        """
        Allows dry runs
        Also allows intentional downgrades
        """
        pass
    def get_versions(self):
        """
        Get versions of plugin
        Filter versions compatible to QGIS version
        """
        pass
    def send_vote(self):
        pass
    def load(self):
        pass
    def unload(self):
        pass
    def reload(self):
        # if loaded ...
        self.unload()
        self.load()
    def _fetch_available_versions(self):
        """HTTP ..."""
        pass
    def _fetch_plugin(self):
        """HTTP ..."""
        pass
    def _fetch_metadata(self):
        """HTTP ..."""
        pass
    def _validate_install(self):
        """
        Post-install or post-update/-downgrade checks of files and folders
        """
        pass
    def _validate_uninstall(self):
        """
        Post-uninstall checks of files and folders
        """
        pass
