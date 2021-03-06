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

from typing import Generator, Iterator

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# IMPORT (Internal)
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

from .abc import (
    plugin_abc,
    pluginrelease_abc,
    settings_abc,
    )
from .backends import backends
from .error import (
    QgistNotAPluginDirectoryError,
    QgistIsInstalledError,
    QgistIsNotInstalledError,
    QgistProtectedError,
    )

from ..error import (
    QgistNotImplementedError,
    QgistTypeError,
    QgistValueError,
    )
from ..util import tr

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# CLASS
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

class dtype_plugin_class(plugin_abc):
    """
    One single plugin

    This class represents a single plugin, i.e. all of its releases from backends and versions.

    Mutable.
    """

    def __init__(self,
        plugin_id, installed_release, available_releases, protected, active, deprecated,
        module = None,
        ):

        if not isinstance(plugin_id, str):
            raise QgistTypeError(tr('"plugin_id" must be a str.'))
        if len(plugin_id) == 0:
            raise QgistValueError(tr('"plugin_id" must not be empty.'))
        if not isinstance(installed_release, pluginrelease_abc) and installed_release is not None:
            raise QgistTypeError(tr('"installed_release" must be a plugin release or None'))
        if not any((isinstance(available_releases, dtype) for dtype in (Generator, Iterator, list, tuple))):
            raise QgistTypeError(tr('"available_releases" must be any of the following: list, tuple, generator, iterator.'))
        available_releases = list(available_releases)
        if not all((isinstance(release, pluginrelease_abc) for release in available_releases)):
            raise QgistTypeError(tr('All available releases must be plugin releases.'))
        if any((release.installed for release in available_releases)):
            raise QgistValueError(tr('An installed release can not be available'))
        if not isinstance(protected, bool):
            raise QgistTypeError(tr('"protected" must be a bool.'))
        if not isinstance(active, bool):
            raise QgistTypeError(tr('"active" must be a bool.'))
        if not isinstance(deprecated, bool):
            raise QgistTypeError(tr('"deprecated" must be a bool.'))

        self._id = plugin_id # unique
        self._installed_release = installed_release
        self._available_releases = available_releases # list of dtype_pluginrelease. Source available (online), matching QGIS version requirement
        self._protected = protected
        self._active = active
        self._deprecated = deprecated
        self._module = module

        self._update_deprecation()

        self._watchdog = None # TODO in release?

    def __repr__(self):

        return (
            '<plugin '
            f'id="{self._id:s}" '
            f'installed={"yes" if self.installed else "no":s} '
            f'active={"yes" if self._active else "no":s} '
            f'available_releases={len(self):d} '
            f'upgradable={"yes" if self.upgradable else "no":s} '
            f'downgradable={"yes" if self.downgradable else "no":s} '
            f'orphan={"yes" if self.orphan else "no":s} '
            f'deprecated={"yes" if self._deprecated else "no":s} '
            f'protected={"yes" if self._protected else "no":s}'
            '>'
            )

    def __len__(self):

        return len(self._available_releases)

    def __contains__(self, test_release):

        if not isinstance(test_release, pluginrelease_abc):
            raise QgistTypeError(tr('"release" must be a release'))

        return any((
            release == test_release
            for release in self._available_releases
            ))

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# PROPERTIES
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

    @property
    def id(self):
        return self._id

    @property
    def installed(self):
        return self._installed_release is not None

    @property
    def protected(self):
        return self._protected

    @property
    def active(self):
        if not self.installed:
            return False
        return self._active
    @active.setter
    def active(self, value):
        if not isinstance(value, bool):
            raise QgistTypeError(tr('"value" must be a bool.'))
        if not self.installed:
            raise QgistIsNotInstalledError(tr('plugin is not installed'))
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
    def installed_release(self):
        if not self.installed:
            raise QgistValueError(tr('plugin is not installed'))
        return self._installed_release

    @property
    def available_releases(self):
        return (release for release in self._available_releases)

    @property
    def upgradable(self):
        if not self.installed:
            return False
        if len(self._available_releases) == 0:
            return False
        return any((
            available_release.version > self._installed_release.version
            for available_release in self._available_releases
            ))

    @property
    def downgradable(self):
        if not self.installed:
            return False
        if len(self._available_releases) == 0:
            return False
        return any((
            available_release.version < self._installed_release.version
            for available_release in self._available_releases
            ))

    @property
    def orphan(self):
        if not self.installed:
            return False
        return all((
            available_release != self._installed_release
            for available_release in self._available_releases
            ))

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# MANAGE RELEASES
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

    def add_release(self, new_release):
        "Add a potentially new and uninstalled but available release"

        if not isinstance(new_release, pluginrelease_abc):
            raise QgistTypeError(tr('"new_release" must be a release'))
        if new_release in self:
            raise QgistValueError(tr('"new_release" is already part of this plugin'))
        if self._id != new_release.id:
            raise QgistValueError(tr('Trying to add a new_release with a different id'))
        if new_release.installed and self.installed:
            raise QgistValueError(tr('Trying to add an installed release to an installed plugin'))

        self._available_releases.append(new_release)
        self._update_deprecation()

    def clear_releases(self):
        "Remove all uninstalled releases"

        self._available_releases.clear()
        self._update_deprecation()

    def _update_deprecation(self):
        "Checks all releases for deprecated flag and taint entire plugin"

        self._deprecated = any((release.deprecated for release in self._available_releases))

        if self._deprecated:
            return
        if not self.installed:
            return

        self._deprecated = self._installed_release.deprecated

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# INSTALL / UNINSTALL
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

    def install(self,
        release = None,
        allow_typechange = False,
        allow_sameversion = False, allow_downgrade = False, allow_update = True,
        ):
        "Installs a plugin release"
        # TODO Should allow dry runs

        if self._protected:
            raise QgistProtectedError(tr('this plugin is protected'))

        if release is None:
            release = self._available_releases[-1] # take the newest from repo with highest priority

        if not isinstance(release, pluginrelease_abc):
            raise QgistTypeError(tr('"release" must be a plugin release'))
        if release.id != self._id:
            raise QgistValueError(tr('"release" does not belong to this plugin'))
        if release not in self:
            raise QgistValueError(tr('"release" is not available'))

        if not isinstance(allow_typechange, bool):
            raise QgistTypeError(tr('"allow_typechange" must be bool'))
        if not isinstance(allow_sameversion, bool):
            raise QgistTypeError(tr('"allow_sameversion" must be bool'))
        if not isinstance(allow_downgrade, bool):
            raise QgistTypeError(tr('"allow_downgrade" must be bool'))
        if not isinstance(allow_update, bool):
            raise QgistTypeError(tr('"allow_update" must be bool'))

        def _uninstall(allow_x, msg):
            if not allow_x:
                raise QgistIsInstalledError(msg)
            if self._installed_release.repo_type != release.repo_type and not allow_typechange:
                raise QgistIsInstalledError(tr('change of repo type not allowed'))
            self.uninstall()

        if self.installed:
            if self._installed_release.version == release.version:
                _uninstall(allow_sameversion, tr('plugin release is already installed'))
            elif self._installed_release.version > release.version:
                _uninstall(allow_downgrade, tr('plugin would be downgraded'))
            elif self._installed_release.version < release.version:
                _uninstall(allow_update, tr('plugin would be updated'))

        release.install()
        self._installed_release = release

    def uninstall(self):
        "Uninstalled the currently installed plugin release"
        # TODO Should allow dry runs

        if self._protected:
            raise QgistProtectedError(tr('this plugin is protected'))
        if not self.installed:
            raise QgistIsNotInstalledError(tr('plugin is not installed'))

        if self._active:
            self.unload()

        self._installed_release.uninstall()
        self._installed_release = None

        # TODO remove settings for this plugin (e.g. active etc)
        # TODO remove from index if orhan (nothing available)

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# LOADING / UNLOADING
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
        if not isinstance(config, settings_abc):
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
            installed_release = installed_release,
            available_releases = tuple(),
            protected = protected,
            active = installed_release.id in plugin_modules.keys(),
            deprecated = installed_release.meta['deprecated'].value,
            module = plugin_modules.get(installed_release.id, None),
            )

    @classmethod
    def from_uninstalled_release(cls, release):

        if not isinstance(release, pluginrelease_abc):
            raise QgistTypeError(tr('"release" must be a plugin release'))
        if release.installed:
            raise QgistValueError(tr('"release" must not be installed'))

        return cls(
            plugin_id = release.id,
            installed_release = None,
            available_releases = (release,),
            protected = False,
            active = False,
            deprecated = release.deprecated,
            module = None,
            )
