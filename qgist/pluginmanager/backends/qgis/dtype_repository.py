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
# IMPORT (Internal)
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

from ...const import (
    CONFIG_DELIMITER,
    REPO_DEFAULT_URL,
    )
from ...dtype_repository_base import dtype_repository_base_class
from ...dtype_settings import dtype_settings_group_class

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

        self._valid = valid # TODO Appears to me meaningless!?
        self._url = url
        self._authcfg = authcfg

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
            repository_type = 'qgis',
            plugin_releases = list(),
            config_group = config_group,
            # SPECIAL:
            valid = config_group.settings.str_to_bool(config_group.get('valid', 'true')),
            authcfg = config_group['authcfg'],
            url = config_group['url'],
        )
