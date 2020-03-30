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

from ..error import QgistNotImplementedError

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# CLASS
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

class dtype_repository_class:
    """
    # Repo

    This is abstract class representing a repository.
    From this, classes for repo types (i.e. plugin sources) are derived.

    Auto-detect (and auto-import) repo types?

    - sources:
        - remote (HTTP, FTP, ...)
        - locally (drive, share, path)
        - "links" (`ln -s`) to local folders for plugins
    - types:
        - pip (through pip API)
        - conda (through conda API)
        - traditional QGIS
    - properties:
        - NAME
        - active/enabled
        - writeable/protected (FALSE for core plugins "repo"/directory and QGIS Python plugins repo)
        - autorefresh (on start)
        - autorefresh_interval
        - AUTH?
        - priority
        - available (i.e. contact to server?)
        - meta ...
        - LIST OF PLUGINS
        - SETTINGS
    """

    def get_all_installed(self):
        raise QgistNotImplementedError()
    def get_all_available(self):
        """
        Available plugins, compatible to QGIS version
        """
        raise QgistNotImplementedError()
    def rename(self, new_name):
        raise QgistNotImplementedError()
    def refresh(self):
        raise QgistNotImplementedError()

    def _fetch_index(self):
        """HTTP ..."""
        pass

    @classmethod
    def from_directory(cls, path, writeable = False):
        # TODO
        return cls()
