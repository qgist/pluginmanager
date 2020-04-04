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

import random

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# IMPORT (Internal)
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

from ...const import (
    CONFIG_DELIMITER,
    CONFIG_GROUP_QGISLEGACY_REPOS,
    REPO_DEFAULT_URL,
    REPO_BACKEND_QGISLEGACYPYTHON,
    )
from ...dtype_repository_base import dtype_repository_base_class
from ...dtype_settings import (
    dtype_settings_group_class,
    dtype_settings_class,
    )

from ....error import (
    QgistTypeError,
    QgistValueError,
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

    REPO_TYPE = REPO_BACKEND_QGISLEGACYPYTHON

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

    @property
    def url(self):
        return self._url

    @classmethod
    def get_repo_config_groups(cls, config):

        if not isinstance(config, dtype_settings_class):
            raise QgistTypeError(tr('"config" must be a "dtype_settings_class" object.'))

        qgislegacy_group = config.get_group(CONFIG_GROUP_QGISLEGACY_REPOS)

        return (
            qgislegacy_group.get_group(repo_id)
            for repo_id in qgislegacy_group.keys_root()
            )

    @classmethod
    def from_default(cls, config):

        name = tr('QGIS Official Python Plugin Repository')
        repo_id = f'{name:s} ({random.randint(2**31, 2**32 - 1):x})' # avoid collisions!

        return cls(
            repo_id = repo_id,
            name = name,
            active = True,
            protected = True,
            repository_type = cls.REPO_TYPE,
            plugin_releases = list(),
            config_group = config.get_group(CONFIG_GROUP_QGISLEGACY_REPOS).get_group(repo_id),
            # SPECIAL
            valid = True,
            authcfg = '', # TODO empty ok?
            url = REPO_DEFAULT_URL,
            )

    @classmethod
    def from_config(cls, config_group):

        if not isinstance(config_group, dtype_settings_group_class):
            raise QgistTypeError(tr('"config_group" is not a group of settings'))

        return cls(
            repo_id = config_group.root.rsplit(CONFIG_DELIMITER, 1)[-1],
            name = config_group.root.rsplit(CONFIG_DELIMITER, 1)[-1],
            active = config_group.settings.str_to_bool(config_group['enabled']),
            protected = config_group.get(
                'protected',
                config_group['url'].strip().lower() == REPO_DEFAULT_URL.strip().lower(),
                ),
            repository_type = cls.REPO_TYPE,
            plugin_releases = list(),
            config_group = config_group,
            # SPECIAL
            valid = config_group.settings.str_to_bool(config_group.get('valid', 'true')),
            authcfg = config_group['authcfg'],
            url = config_group['url'],
        )
