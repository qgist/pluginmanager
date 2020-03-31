# -*- coding: utf-8 -*-

"""

QGIST PLUGIN MANAGER
QGIS Plugin for Managing QGIS Plugins
https://github.com/qgist/pluginmanager

    qgist/pluginmanager/dtype_repository.py: Repository data type

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

from ..error import (
    QgistNotImplementedError,
    QgistValueError,
    QgistTypeError,
    )
from ..util import tr

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# CLASS
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

class dtype_repository_base_class:
    """
    # Repo

    This is abstract class representing a repository.
    From this, classes for repo types (i.e. plugin sources) are derived.

    Mutable.
    """

    def __init__(self, *args, **kwargs): # TODO

        self._id = '' # str (unique)
        self._name = '' # str (enable translations!)
        self._active = True # bool
        self._protected = False # bool
        self._repository_type = '' # str: {backends: conda, pip, conda, qgis}

        self._plugins = [] # list of all relevant plugins

    def __repr__(self):

        return (
            '<repository '
            f'id="{self._id:s}" name="{self._name:s}" type="{self._repository_type:s}" '
            f'protected={"yes" if self._protected else "no":s} '
            f'active={"yes" if self._active else "no":s}'
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
    @name.setter
    def name(self, value):
        if not isinstance(value, str):
            raise QgistTypeError(tr('New value of "name" must be a str.'))
        if len(value) == 0:
            raise QgistValueError(tr('New value of "name" must not be empty.'))
        self._name = value

    @property
    def active(self):
        return self._active

    @property
    def protected(self):
        return self._protected

    @property
    def repository_type(self):
        return self._repository_type

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# MANAGEMENT
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

    def get_all_installed_plugins(self):
        "Currently installed plugins"

        return (plugin for plugin in self._plugins if plugin.installed)

    def get_all_available_plugins(self):
        "Available plugins, compatible to QGIS version"

        if not self._active:
            return tuple()
        return (plugin for plugin in self._plugins if plugin.available)

    def refresh_index(self):
        "Rebuild index and/or reload metadata"

        raise QgistNotImplementedError()

    def remove(self):
        "Run cleanup actions e.g. in config before repo is removed"

        raise QgistNotImplementedError()

    def _fetch_index(self):
        """HTTP ..."""
        pass

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# PRE-CONSTRUCTOR
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

    @classmethod
    def from_directory(cls, path, writeable = False):
        raise QgistNotImplementedError()

    @classmethod
    def from_userinput(cls):
        raise QgistNotImplementedError()

    @classmethod
    def from_config(cls, config):
        raise QgistNotImplementedError()
