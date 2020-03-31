# -*- coding: utf-8 -*-

"""

QGIST PLUGIN MANAGER
QGIS Plugin for Managing QGIS Plugins
https://github.com/qgist/pluginmanager

    qgist/pluginmanager/dtype_index.py: Repository index data type

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

from .backends import backends
from .dtype_settings import dtype_settings_class

from ..error import (
    QgistTypeError,
    QgistValueError,
    )
from ..util import tr

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# CLASS
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

class dtype_index_class:
    """
    # Index of repos

    - properties:
        - list of present/registered repos
        - allow experimental
        - allow deprecated
        - SETTINGS
        - actions (stuff that must be committed or discarded) ... its own class?
    """

    def __init__(self, config):

        if not isinstance(config, dtype_settings_class):
            raise QgistTypeError(tr('"config" must be a "dtype_settings_class" object.'))

        self._config = config
        self._repos = []

    def __repr__(self):

        return f'<index ({id(self):x})>'

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# PROPERTIES
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

    @property
    def repos(self):
        return (repo for repo in self._repos)

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# MANAGEMENT: REPO
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

    def add_repo(self, repo_type, **kwargs):
        """
        What type? Get right class, get configuration or user input.
        """

        pass

    def get_repo(self, repo_id):

        if not isinstance(repo_id, str):
            raise QgistTypeError(tr('"repo_id" must be a str.'))
        if len(repo_id) == 0:
            raise QgistValueError(tr('"repo_id" must not be empty.'))
        if repo_id not in (repo.id for repo in self._repos):
            raise QgistValueError(tr('"repo_id" is unknown. There is no such repository.'))

        return {repo.id: repo for repo in self._repos}[repo_id]

    def remove_repo(self, repo_id):

        repo = self.get_repo(repo_id)
        repo.remove()
        self._repos.remove(repo)

    def refresh_repos(self):
        """Reload index of every repo"""

        for repo in self._repos:
            repo.refresh()

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# MANAGEMENT: PLUGINS
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
