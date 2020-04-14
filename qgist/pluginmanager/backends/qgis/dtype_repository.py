# -*- coding: utf-8 -*-

"""

QGIST PLUGIN MANAGER
QGIS Plugin for Managing QGIS Plugins
https://github.com/qgist/pluginmanager

    qgist/pluginmanager/backends/qgis/dtype_repository.py: Repository data type

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

import glob
import multiprocessing
import os
import random
import sys

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# IMPORT (External)
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

import xmltodict

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# IMPORT (Internal)
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

from .dtype_pluginrelease import dtype_pluginrelease_class

from ...abc import (
    settings_abc,
    settings_group_abc,
    )
from ...const import (
    CONFIG_DELIMITER,
    CONFIG_GROUP_QGISLEGACY_REPOS,
    REPO_DEFAULT_URL,
    REPO_BACKEND_QGISLEGACYPYTHON,
    )
from ...error import (
    QgistNotADirectoryError,
    )
from ...dtype_plugin import dtype_plugin_class
from ...dtype_repository_base import dtype_repository_base_class
from ...dtype_version import dtype_version_class

from ....error import (
    QgistTypeError,
    QgistValueError,
    )
from ....qgis_api import (
    get_home_python_path,
    get_python_path,
    get_qgis_version,
    request_data,
    )
from ....util import tr

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# CLASS
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

class dtype_repository_class(dtype_repository_base_class):
    """
    - sources
        - remote (HTTP, FTP, ...)
        - locally (drive, share, path)
        - "links" (`ln -s`) to local folders for plugins
    - special properties
        - AUTH?
    """

    _repo_type = REPO_BACKEND_QGISLEGACYPYTHON

    def __init__(self, *args,
        valid = None, authcfg = None, url = None,
        **kwargs,
        ):

        super().__init__(*args, **kwargs)

        if not isinstance(valid, bool):
            raise QgistTypeError(tr('"valid" must be bool'))
        if not isinstance(authcfg, str):
            raise QgistTypeError(tr('"authcfg" must be str'))
        if not isinstance(url, str):
            raise QgistTypeError(tr('"url" must be str'))
        if not url.lower().startswith('http://') and not url.lower().startswith('https://'):
            raise QgistValueError(tr(''))

        self._valid = valid # TODO Appears to be meaningless!?
        self._url = url
        self._authcfg = authcfg

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# SPECIAL PROPERTIES (ONLY THIS REPO TYPE)
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

    @property
    def url(self):
        return self._url

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# MANAGEMENT & EXPORT
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

    def refresh(self):
        "Refresh index, i.e. reload metadata from remote source"

        qgis_version = dtype_version_class.from_qgisversion(get_qgis_version(), fix_plugin_compatibility = True)

        raw_xml_bytes = request_data(
            f'{self._url:s}?qgis={qgis_version[0]:s}.{qgis_version[1]:s}',
            self._authcfg,
            )
        raw_xml = raw_xml_bytes.decode('utf-8')
        raw_xml = raw_xml.replace('& ', '&amp; ') # From plugin installer: Fix lonely ampersands in metadata
        tree = xmltodict.parse(raw_xml)
        release_id_set = {
            dtype_pluginrelease_class.from_xmldict(dict(release_dict)).id
            for release_dict in tree['plugins']['pyqgis_plugin']
            }

        dict_release_list_list = []
        with multiprocessing.Pool(processes = multiprocessing.cpu_count()) as p:
            dict_release_list_list.extend(p.imap_unordered(
                func = self._request_dict_releases_per_plugin,
                iterable = (
                    (f'{self._url:s}?package_name={release_id:s}&qgis={qgis_version[0]:s}.{qgis_version[1]:s}', self._authcfg)
                    for release_id in release_id_set
                    ),
                chunksize = 50,
                ))

        all_releases = []
        for dict_release_list in dict_release_list_list:
            all_releases.extend((
                dtype_pluginrelease_class.from_xmldict(dict_release)
                for dict_release in dict_release_list
                ))

        self._plugin_releases.clear()
        self._plugin_releases.extend(all_releases)
        self.to_config()

    @staticmethod
    def _request_dict_releases_per_plugin(param):

        url, authcfg = param
        raw_xml_bytes = request_data(url, authcfg)

        raw_xml = raw_xml_bytes.decode('utf-8')
        raw_xml = raw_xml.replace('& ', '&amp; ') # From plugin installer: Fix lonely ampersands in metadata
        tree = xmltodict.parse(raw_xml)

        if isinstance(tree['plugins']['pyqgis_plugin'], list): # more than one
            return [dict(release_dict) for release_dict in tree['plugins']['pyqgis_plugin']]
        return [dict(tree['plugins']['pyqgis_plugin'])] # just one

    # def remove(self):
    #     "Run cleanup actions e.g. in config before repo is removed"
    #
    #     raise QgistNotImplementedError()

    def to_config(self):
        "Write repository to configuration"

        super().to_config()

        self._config_group['valid'] = self._config_group.settings.bool_to_str(self._valid, style = 'truefalse')
        self._config_group['authcfg'] = self._authcfg
        self._config_group['url'] = self._url

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# CLASS-LEVEL API
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

    @classmethod
    def get_repo_config_groups(cls, config):

        if not isinstance(config, settings_abc):
            raise QgistTypeError(tr('"config" must be a "dtype_settings_class" object.'))

        qgislegacy_group = config.get_group(CONFIG_GROUP_QGISLEGACY_REPOS)

        return (
            qgislegacy_group.get_group(repo_id)
            for repo_id in qgislegacy_group.keys_root()
            )

    @classmethod
    def find_plugins(cls, config, protected, plugin_modules):
        """
        Based on:
            - `/src/python/qgspythonutilsimpl.cpp`, `QgsPythonUtilsImpl::checkSystemImports()`
            - `/python/utils.py`, `findPlugins` and `updateAvailablePlugins`
        Returns: All installed plugins, one (installed) release each
        """

        if not isinstance(config, settings_abc):
            raise QgistTypeError(tr('"config" must be a "dtype_settings_class" object.'))
        if not isinstance(protected, bool):
            raise QgistTypeError(tr('"protected" must be a bool'))
        if not isinstance(plugin_modules, dict):
            raise QgistTypeError(tr('"plugin_modules" must be a dict'))
        if not all((isinstance(plugin_id, str) for plugin_id in plugin_modules.keys())):
            raise QgistTypeError(tr('Every plugin_id in "plugin_modules" must be str'))

        if protected:
            plugin_paths = (os.path.join(get_python_path(), 'plugins'),)
        else:
            plugin_paths = (*_get_extra_plugins_paths(), os.path.join(get_home_python_path(), 'plugins'))

        plugins = []

        for plugin_path in plugin_paths:
            for entry in glob.glob(plugin_path + '/*'):
                if not dtype_pluginrelease_class.is_python_plugin_dir(entry):
                    continue
                plugins.append(dtype_plugin_class.from_installed(
                    entry, config, cls._repo_type, protected, plugin_modules,
                    ))

        return (plugin for plugin in plugins)

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# PRE-CONSTRUCTOR
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

    @classmethod
    def from_default(cls, config):

        if not isinstance(config, settings_abc):
            raise QgistTypeError(tr('"config" is not settings'))

        name = tr('QGIS Official Python Plugin Repository')
        repo_id = f'{name:s} ({random.randint(2**31, 2**32 - 1):x})' # avoid collisions!

        return cls(
            repo_id = repo_id,
            name = name,
            active = True,
            protected = True,
            plugin_releases = tuple(), # This is new, there is no cache.
            config_group = config.get_group(CONFIG_GROUP_QGISLEGACY_REPOS).get_group(repo_id),
            # SPECIAL
            valid = True,
            authcfg = '', # TODO empty ok?
            url = REPO_DEFAULT_URL,
            )

    @classmethod
    def from_config(cls, config_group):

        if not isinstance(config_group, settings_group_abc):
            raise QgistTypeError(tr('"config_group" is not a group of settings'))

        protected = config_group.settings.str_to_bool(config_group.get('protected', None))
        if protected is None:
            protected = (config_group['url'].strip().lower() == REPO_DEFAULT_URL.strip().lower())
        else:
            protected = False

        return cls(
            repo_id = config_group.root.rsplit(CONFIG_DELIMITER, 1)[-1],
            name = config_group.root.rsplit(CONFIG_DELIMITER, 1)[-1], # TODO look for name!
            active = config_group.settings.str_to_bool(config_group['enabled']),
            protected = protected,
            plugin_releases = cls.get_releases_from_config_cache(config_group, cls._repo_type),
            config_group = config_group,
            # SPECIAL
            valid = config_group.settings.str_to_bool(config_group.get('valid', 'true')),
            authcfg = config_group['authcfg'],
            url = config_group['url'],
            )

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# ROUTINES (ONLY THIS REPO TYPE)
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

def _get_extra_plugins_paths():

    if 'QGIS_PLUGINPATH' not in os.environ.keys():
        return tuple()

    paths = os.environ['QGIS_PLUGINPATH']
    delimiter = ';' if sys.platform.startswith('win') else ':'
    checked_paths = []

    python_path = os.path.join(get_python_path(), 'plugins')

    for path in paths.split(delimiter):
        path = os.path.abspath(path)
        if not os.path.isdir(path):
            raise QgistNotADirectoryError(tr('The extra plugin path does not exist') + f': {path:s}')
        if path == python_path:
            raise QgistValueError(tr('"QGIS_PLUGINPATH" contains a protected path'))
        checked_paths.append(path)

    return (path for path in checked_paths)
