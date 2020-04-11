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

from .const import (
    # CONFIG_GROUP_MANAGER_REPOS,
    CONFIG_KEY_ALLOW_DEPRECATED,
    CONFIG_KEY_ALLOW_EXPERIMENTAL,
    REPO_BACKEND_QGISLEGACYCPP,
    REPO_BACKEND_QGISLEGACYPYTHON,
    REPO_DEFAULT_URL,
    )
from .backends import backends
from .error import (
    QgistPluginIdCollisionError,
    QgistRepoError,
    )
from .dtype_plugin import dtype_plugin_class
from .dtype_repository_base import dtype_repository_base_class
from .dtype_settings import dtype_settings_class

from ..error import (
    QgistTypeError,
    QgistValueError,
    )
from ..qgis_api import get_plugin_modules
from ..util import tr

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# CLASS: INDEX
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

class dtype_index_class:
    """
    Index of repositories

    Mutable.
    """

    def __init__(self, config):

        if not isinstance(config, dtype_settings_class):
            raise QgistTypeError(tr('"config" must be a "dtype_settings_class" object.'))

        self._config = config
        self._repos = [] # From high to low priority
        self._plugins = {} # Individual plugins, not their releases

        # TODO <HACK>
        # remove this eventually - Plugin Manager should manage this on its own
        # dict by plugin_id: reference on imported Python plugin modules
        self._plugin_modules = get_plugin_modules()
        # TODO </HACK>

        self._allow_deprecated = self._config.str_to_bool(self._config[CONFIG_KEY_ALLOW_DEPRECATED])
        self._allow_experimental = self._config.str_to_bool(self._config[CONFIG_KEY_ALLOW_EXPERIMENTAL])

        self.rebuild()

    def __repr__(self):

        return f'<index ({id(self):x}) repos={self.len_repos:d} plugins={self.len_plugins:d}>'

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# PROPERTIES
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

    @property
    def repos(self):
        return (repo for repo in self._repos)

    @property
    def len_repos(self):
        return len(self._repos)

    @property
    def plugins(self):
        return (plugin for plugin in self._plugins.values())

    @property
    def len_plugins(self):
        return len(self._plugins)

    @property
    def allow_deprecated(self):
        return self._allow_deprecated
    @allow_deprecated.setter
    def allow_deprecated(self, value):
        if not isinstance(value, bool):
            raise QgistTypeError(tr('value is not bool'))
        self._allow_deprecated = value
        self._config[CONFIG_KEY_ALLOW_DEPRECATED] = self._config.bool_to_str(value, style = 'truefalse')

    @property
    def allow_experimental(self):
        return self._allow_experimental
    @allow_experimental.setter
    def allow_experimental(self, value):
        if not isinstance(value, bool):
            raise QgistTypeError(tr('value is not bool'))
        self._allow_experimental = value
        self._config[CONFIG_KEY_ALLOW_EXPERIMENTAL] = self._config.bool_to_str(value, style = 'truefalse')

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# MANAGEMENT: INDEX
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

    def rebuild(self):
        "Rebuild index of repos and plugins"

        self._repos.clear()
        self._plugins.clear()
        # TODO what about self._plugin_modules?

        self._rebuild_plugins()
        self._rebuild_repos()

        self._ensure_qgislegacypython_default_repo()
        self._ensure_qgislegacycpp_repo()

        # self._refresh_repos() # TODO activate depending on settings

        self._match_releases_from_repos_to_plugins()

    def _rebuild_plugins(self):

        for repo_type in backends.keys():
            for protected in (True, False):
                found_plugins = {
                    plugin.id: plugin
                    for plugin in self.get_repo_class(repo_type).find_plugins(
                        self._config, protected = protected,
                        # TODO <HACK>
                        # remove this eventually - Plugin Manager should load plugins
                        # on its own when index is initialized (at QGIS startup)
                        plugin_modules = self._plugin_modules.copy(),
                        # TODO </HACK>
                        )
                    }
                if len(found_plugins.keys() & self._plugins.keys()) != 0:
                    raise QgistPluginIdCollisionError(tr('Two or more plugins with identical ID'))
                self._plugins.update(found_plugins)

    def _rebuild_repos(self):

        for repo_type in backends.keys():
            for config_group in self.get_repo_class(repo_type).get_repo_config_groups(self._config):
                self.add_repo(self.create_repo(
                    config_group,
                    repo_type = repo_type, method = 'config',
                    ))

    def _ensure_qgislegacypython_default_repo(self):

        if not any((
            repo.url == REPO_DEFAULT_URL
            for repo in self._repos if repo.repo_type == REPO_BACKEND_QGISLEGACYPYTHON
            )):
            self.add_repo(self.create_repo(
                self._config,
                repo_type = REPO_BACKEND_QGISLEGACYPYTHON, method = 'default',
                ))

    def _ensure_qgislegacycpp_repo(self):

        if not any((
            repo.repo_type == REPO_BACKEND_QGISLEGACYCPP
            for repo in self._repos
            )):
            self.add_repo(self.create_repo(
                self._config,
                repo_type = REPO_BACKEND_QGISLEGACYCPP, method = 'default',
                ))

        if len([repo for repo in self._repos if repo.repo_type == REPO_BACKEND_QGISLEGACYCPP]) != 1:
            raise QgistRepoError(tr('There must be exactly one C++ repository.'))

    def _refresh_repos(self):

        # TODO refresh option from config

        for repo in self._repos:
            repo.refresh()

    def _match_releases_from_repos_to_plugins(self):

        # TODO Remove plugins with zero releases?

        for plugin in self._plugins.values():
            plugin.clear_releases()

        for repo in self._repos:
            for release in sorted(repo.plugin_releases, key = lambda x: x.version):
                if release.id in self._plugins.keys():
                    self._plugins[release.id].add_release(release)
                else:
                    self._plugins[release.id] = dtype_plugin_class.from_uninstalled_release(release)

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# MANAGEMENT: REPOSITORIES
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

    def add_repo(self, repo):
        "Add a repository"

        if not isinstance(repo, dtype_repository_base_class):
            raise QgistTypeError(tr('"repo" is not a repo'))
        if repo.id in (present_repo.id for present_repo in self._repos):
            raise QgistValueError(tr('"repo" can not be added - its id is already in list'))

        self._repos.insert(0, repo) # Add to list at the end, i.e. with lowest priority

    @classmethod
    def create_repo(cls, *args, repo_type = None, method = None, **kwargs):
        "Initialize repository based on type, method and arbitrary parameters"

        repository_class = cls.get_repo_class(repo_type)

        if not isinstance(method, str):
            raise QgistTypeError(tr('"method" must be a str.'))

        if method not in (item[5:] for item in dir(repository_class) if item.startswith('from_')):
            raise QgistValueError(tr('"method" is unknown.'))
        method = getattr(repository_class, f'from_{method:s}')
        if not hasattr(method, '__call__'):
            raise QgistTypeError(tr('"method" can not be called.'))

        return method(*args, **kwargs) # TODO: Catch user abort

    def change_repo_priority(self, repo_id, direction):
        "Repository can be moved up (higher priority) or down (lower priority) by one"

        if not isinstance(direction, int):
            raise QgistTypeError(tr('"direction" must be a int.'))
        if direction not in (1, -1):
            raise QgistValueError(tr('"direction" must either be 1 or -1.'))

        repo = self.get_repo(repo_id)
        index = self._repos.index(repo)

        if self.len_repos < 2:
            return
        if index == 0 and direction == -1:
            return
        if index == (self.len_repos - 1) and direction == 1:
            return

        self._repos[index + direction], self._repos[index] = self._repos[index], self._repos[index + direction]

    def get_repo(self, repo_id):
        "Get repository from index by id (if it is present)"

        if not isinstance(repo_id, str):
            raise QgistTypeError(tr('"repo_id" must be a str.'))
        if len(repo_id) == 0:
            raise QgistValueError(tr('"repo_id" must not be empty.'))
        if repo_id not in (repo.id for repo in self._repos):
            raise QgistValueError(tr('"repo_id" is unknown. There is no such repository.'))

        return {repo.id: repo for repo in self._repos}[repo_id]

    @staticmethod
    def get_repo_class(repo_type):

        if not isinstance(repo_type, str):
            raise QgistTypeError(tr('"repo_type" must be a str.'))
        if repo_type not in backends.keys():
            raise QgistValueError(tr('"repo_type" is unknown.'))

        if not backends[repo_type].module_loaded:
            backends[repo_type].load_module()

        return backends[repo_type].dtype_repository_class

    def remove_repo(self, repo_id):
        "Remove repository from index by id (if it is present)"

        repo = self.get_repo(repo_id)
        repo.remove()
        self._repos.remove(repo)

    # def refresh_repos(self):
    #     "Reload index of every repo"
    #
    #     for repo in self._repos:
    #         repo.refresh()

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# MANAGEMENT: PLUGINS
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

    def add_plugin(self, plugin):
        "Add a plugin to index"

        if not isinstance(plugin, dtype_plugin_class):
            raise QgistTypeError(tr('"plugin" is not a plugin'))
        if plugin.id in self._plugins.keys():
            raise QgistValueError(tr('"plugin" can not be added - it is already in dict'))

        self._plugins[plugin.id] = plugin

    def get_plugin(self, plugin_id):
        "Get a plugin from index by id"

        if not isinstance(plugin_id, str):
            raise QgistTypeError(tr('"plugin_id" must be a str.'))
        if len(plugin_id) == 0:
            raise QgistValueError(tr('"plugin_id" must not be empty.'))
        if plugin_id not in self._plugins.keys():
            raise QgistValueError(tr('"plugin_id" is unknown. There is no such plugin.'))

        return self._plugins[plugin_id]

    # def remove_plugin(self, plugin_id):
    #
    #     pass

    def get_all_installed_plugins(self):
        "Currently installed plugins"

        return (plugin for plugin in self._plugins.values() if plugin.installed)

    def get_all_available_plugins(self):
        "Available plugins, compatible to QGIS version"

        return (plugin for plugin in self._plugins.values() if plugin.available)
