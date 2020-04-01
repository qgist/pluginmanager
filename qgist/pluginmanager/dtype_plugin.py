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
# IMPORT (Internal)
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

from .dtype_repository import dtype_repository_base_class
from .dtype_settings import dtype_settings_class
from .dtype_version import dtype_version_class

from ..error import (
    QgistNotImplementedError,
    QgistTypeError,
    QgistValueError,
    )
from ..util import tr

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# CLASS
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

class dtype_plugin_base_class:
    """
    # One single plugin

    This is abstract class representing a plugin (all of its versions).
    From this, classes for plugin types (i.e. plugin sources) are derived.

    Mutable.
    """

    def __init__(self,
        plugin_id, name, installed, installed_version,
        protected, active, deprecated, has_processingprovider,
        repo, config,
        ):

        if not isinstance(plugin_id, str):
            raise QgistTypeError(tr('"plugin_id" must be a str.'))
        if len(plugin_id) == 0:
            raise QgistValueError(tr('"plugin_id" must not be empty.'))
        if not isinstance(name, str):
            raise QgistTypeError(tr('"name" must be a str.'))
        if len(name) == 0:
            raise QgistValueError(tr('"name" must not be empty.'))
        if not isinstance(installed, bool):
            raise QgistTypeError(tr('"installed" must be a bool.'))
        if installed and not isinstance(installed_version, dtype_version_class):
            raise QgistTypeError(tr('plugin is installed, i.e. "installed_version" must be a version.'))
        if not installed and installed_version is not None:
            raise QgistTypeError(tr('plugin is not installed, i.e. "installed_version" must be None.'))
        if not isinstance(protected, bool):
            raise QgistTypeError(tr('"protected" must be a bool.'))
        if not isinstance(active, bool):
            raise QgistTypeError(tr('"active" must be a bool.'))
        if not isinstance(deprecated, bool):
            raise QgistTypeError(tr('"deprecated" must be a bool.'))
        if not isinstance(has_processingprovider, bool):
            raise QgistTypeError(tr('"has_processingprovider" must be a bool.'))
        if not isinstance(repo, dtype_repository_base_class):
            raise QgistTypeError(tr('"repo" must be a repository.'))
        if not isinstance(config, dtype_settings_class):
            raise QgistTypeError(tr('"config" must be a "dtype_settings_class" object.'))

        self._id = plugin_id # unique
        self._name = name # TODO enable translations!
        self._installed = installed
        self._installed_version = installed_version
        self._protected = protected
        self._active = active
        self._deprecated = deprecated
        self._has_processingprovider = has_processingprovider
        self._repo = repo # parent repository

        self._config = config

        # Implement in derived class!
        self._available = None # bool. Always static? Source available (online), matching QGIS version requirement
        self._watchdog = None # bool
        self._available_versions = [] # list of dtype_version. Source available (online), matching QGIS version requirement

    def __repr__(self):

        return (
            '<plugin '
            f'id="{self._id:s}" name="{self._name:s}" '
            f'installed={"yes" if self._installed else "no":s} '
            f'active={"yes" if self._active else "no":s} '
            f'deprecated={"yes" if self._deprecated else "no":s} '
            f'protected={"yes" if self._protected else "no":s}'
            '>'
            )

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# PROPERTIES
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name

    @property
    def installed(self):
        return self._installed
    @installed.setter
    def installed(self, value):
        if not isinstance(value, bool):
            raise QgistTypeError(tr('"value" must be a bool.'))
        if value == self._installed:
            return
        if value:
            self.install()
        else:
            self.uninstall()

    @property
    def protected(self):
        return self._protected
    @protected.setter
    def protected(self, value):
        if not isinstance(value, bool):
            raise QgistTypeError(tr('"value" must be a bool.'))
        if not self._installed:
            raise QgistValueError(tr('plugin is not installed'))
        self._protected = value

    @property
    def active(self):
        return self._active
    @active.setter
    def active(self, value):
        if not isinstance(value, bool):
            raise QgistTypeError(tr('"value" must be a bool.'))
        if value == self._active:
            return
        if value:
            self.load()
        else:
            self.unload()

    @property
    def deprecated(self):
        return self._deprecated

    @property
    def has_processingprovider(self):
        return self._has_processingprovider

    @property
    def available(self):
        return self._available

    @property
    def repo(self):
        return self._repo

    @property
    def installed_version(self):
        if not self._installed:
            raise QgistValueError(tr('plugin is not installed'))
        if not isinstance(self._installed_version, dtype_version_class):
            raise QgistValueError(tr('internal error: plugin is installed but has no version'))
        return self._installed_version

    @property
    def available_versions(self):
        return (version for version in self._available_versions)

    @property
    def upgradable(self):
        if not self._installed:
            return False
        if len(self._available_versions) == 0:
            return False
        if not isinstance(self._installed_version, dtype_version_class):
            raise QgistValueError(tr('internal error: plugin is installed but has no version'))
        return any((version > self._installed_version for version in self._available_versions))

    @property
    def downgradable(self):
        if not self._installed:
            return False
        if len(self._available_versions) == 0:
            return False
        if not isinstance(self._installed_version, dtype_version_class):
            raise QgistValueError(tr('internal error: plugin is installed but has no version'))
        return any((version < self._installed_version for version in self._available_versions))

    @property
    def orphan(self):
        if not self._installed:
            return False
        if not isinstance(self._installed_version, dtype_version_class):
            raise QgistValueError(tr('internal error: plugin is installed but has no version'))
        return all((version != self._installed_version for version in self._available_versions))

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# INSTALL / UNINSTALL
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

    def install(self):
        """
        Allows dry runs
        Sets installed to True!
        """
        raise QgistNotImplementedError()

    def uninstall(self):
        """
        Allows dry runs
        Sets installed to False!
        """
        raise QgistNotImplementedError()

    def upgrade(self, version):
        """
        Allows dry runs
        Also allows (intentional) downgrades
        """
        raise QgistNotImplementedError()

    def get_versions(self):
        """
        Get versions of plugin
        Filter versions compatible to QGIS version
        """
        raise QgistNotImplementedError()

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# VOTING
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

    def load(self):
        """
        Loads, i.e. imports plugin (that is actually a Python module), and calls plugin's `initGui`
        Sets active to True!
        """
        raise QgistNotImplementedError()

    def unload(self):
        """
        Triggers plugin's `unload` method and attempts to "unimport" it.
        Sets active to False!
        """
        raise QgistNotImplementedError()

    def reload(self):
        """
        Triggers an unload/load sequence.
        """
        self.unload()
        self.load()

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# VOTING
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

    def send_vote(self):
        """
        Only relevant if plugin comes from QGIS package repo.
        """
        raise QgistNotImplementedError()

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# ETC
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

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
