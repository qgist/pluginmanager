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
# IMPORT (Python Standard Library)
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

import os

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# IMPORT (Python Standard Library)
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

from typing import Generator, Iterator

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# IMPORT (Internal)
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

from .backends import backends
from .error import QgistNotAPluginDirectoryError
from .dtype_pluginrelease_base import dtype_pluginrelease_base_class
from .dtype_settings import dtype_settings_class

from ..error import (
    QgistNotImplementedError,
    QgistTypeError,
    QgistValueError,
    )
from ..util import tr

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# CLASS
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

class dtype_plugin_class:
    """
    One single plugin

    This class represents a single plugin, i.e. all of its releases from backends and versions.

    Mutable.
    """

    def __init__(self,
        plugin_id, installed, installed_release, available_releases, protected, active, deprecated,
        module = None,
        ):

        if not isinstance(plugin_id, str):
            raise QgistTypeError(tr('"plugin_id" must be a str.'))
        if len(plugin_id) == 0:
            raise QgistValueError(tr('"plugin_id" must not be empty.'))
        if not isinstance(installed, bool):
            raise QgistTypeError(tr('"installed" must be a bool.'))
        if installed and not isinstance(installed_release, dtype_pluginrelease_base_class):
            raise QgistTypeError(tr('plugin is installed, i.e. "installed_release" must be a plugin release.'))
        if not installed and installed_release is not None:
            raise QgistTypeError(tr('plugin is not installed, i.e. "installed_release" must be None.'))
        if not any((isinstance(available_releases, dtype) for dtype in (Generator, Iterator, list, tuple))):
            raise QgistTypeError(tr('"available_releases" must be any of the floowing: list, tuple, generator, iterator.'))
        available_releases = list(available_releases)
        if not all((isinstance(release, dtype_pluginrelease_base_class) for release in available_releases)):
            raise QgistTypeError(tr('All available releases must be plugin releases.'))
        if not isinstance(protected, bool):
            raise QgistTypeError(tr('"protected" must be a bool.'))
        if not isinstance(active, bool):
            raise QgistTypeError(tr('"active" must be a bool.'))
        if not isinstance(deprecated, bool):
            raise QgistTypeError(tr('"deprecated" must be a bool.'))

        # TODO check/inspect "module"?

        self._id = plugin_id # unique
        self._installed = installed
        self._installed_release = installed_release
        self._available_releases = available_releases # list of dtype_pluginrelease. Source available (online), matching QGIS version requirement
        self._protected = protected
        self._active = active
        self._deprecated = deprecated
        self._module = module

        # TODO Implement in derived class!
        self._available = None # bool. Always static? Source available (online), matching QGIS version requirement
        self._watchdog = None # bool

    def __repr__(self):

        return (
            '<plugin '
            f'id="{self._id:s}" '
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
    def module(self):
        return self._module

    @property
    def available(self):
        return self._available

    @property
    def installed_release(self):
        if not self._installed:
            raise QgistValueError(tr('plugin is not installed'))
        if not isinstance(self._installed_release, dtype_pluginrelease_base_class):
            raise QgistValueError(tr('internal error: plugin is installed but has no release'))
        return self._installed_release

    @property
    def available_releases(self):
        return (release for release in self._available_releases)

    @property
    def upgradable(self):
        if not self._installed:
            return False
        if len(self._available_releases) == 0:
            return False
        if not isinstance(self._installed_release, dtype_pluginrelease_base_class):
            raise QgistValueError(tr('internal error: plugin is installed but has no release'))
        return any((
            available_release.version > self._installed_release.version
            for available_release in self._available_releases
            ))

    @property
    def downgradable(self):
        if not self._installed:
            return False
        if len(self._available_releases) == 0:
            return False
        if not isinstance(self._installed_release, dtype_pluginrelease_base_class):
            raise QgistValueError(tr('internal error: plugin is installed but has no release'))
        return any((
            available_release.version < self._installed_release.version
            for available_release in self._available_releases
            ))

    @property
    def orphan(self):
        if not self._installed:
            return False
        if not isinstance(self._installed_release, dtype_pluginrelease_base_class):
            raise QgistValueError(tr('internal error: plugin is installed but has no release'))
        return all((
            available_release.version != self._installed_release.version
            for available_release in self._available_releases
            ))

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# INSTALL / UNINSTALL
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

    def install(self):
        """
        Allows dry runs
        Sets installed to True!
        """
        raise QgistNotImplementedError()

    def validate_install(self):
        """
        Post-install or post-update/-downgrade checks of files and folders
        """
        raise QgistNotImplementedError()

    def uninstall(self):
        """
        Allows dry runs
        Sets installed to False!
        """
        raise QgistNotImplementedError()

    def validate_uninstall(self):
        """
        Post-uninstall checks of files and folders
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
# PRE-CONSTRUCTOR
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

    @classmethod
    def from_installed(cls, path, config, repo_type, protected, plugin_modules):

        if not isinstance(repo_type, str):
            raise QgistTypeError(tr('"repo_type" must be str'))
        if repo_type not in backends.keys():
            raise QgistValueError(tr('Unknown repo type'))

        if not backends[repo_type].module_loaded:
            backends[repo_type].load_module()

        if not isinstance(path, str):
            raise QgistTypeError(tr('"path" must be str'))
        if not backends[repo_type].dtype_pluginrelease_class.is_python_plugin_dir(path):
            raise QgistNotAPluginDirectoryError(tr('"path" does not point to a plugin'))
        if not isinstance(config, dtype_settings_class):
            raise QgistTypeError(tr('"config" must be a "dtype_settings_class" object.'))
        if not isinstance(protected, bool):
            raise QgistTypeError(tr('"protected" must be a bool'))
        if not isinstance(plugin_modules, dict):
            raise QgistTypeError(tr('"plugin_modules" must be a dict'))
        if not all((isinstance(plugin_id, str) for plugin_id in plugin_modules.keys())):
            raise QgistTypeError(tr('Every plugin_id in "plugin_modules" must be str'))

        installed_release = backends[repo_type].dtype_pluginrelease_class.from_installed(path, config)

        return cls(
            plugin_id = installed_release.id,
            installed = True,
            installed_release = installed_release,
            available_releases = (installed_release,),
            protected = protected,
            active = installed_release.id in plugin_modules.keys(),
            deprecated = installed_release.meta['deprecated'].value,
            module = plugin_modules.get(installed_release.id, None),
            )
