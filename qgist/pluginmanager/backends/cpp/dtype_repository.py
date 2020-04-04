# -*- coding: utf-8 -*-

"""

QGIST PLUGIN MANAGER
QGIS Plugin for Managing QGIS Plugins
https://github.com/qgist/pluginmanager

    qgist/pluginmanager/backends/cpp/dtype_repository.py: Repository data type

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
    REPO_BACKEND_QGISLEGACYCPP,
    CONFIG_GROUP_MANAGER_REPOS,
    )
from ...dtype_repository_base import dtype_repository_base_class
from ...dtype_settings import dtype_settings_class

from ....error import QgistTypeError
from ....util import tr

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# CLASS
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

class dtype_repository_class(dtype_repository_base_class):

    REPO_TYPE = REPO_BACKEND_QGISLEGACYCPP

    @classmethod
    def find_plugins(cls, config):

        return tuple() # TODO

    @classmethod
    def from_default(cls, config):

        if not isinstance(config, dtype_settings_class):
            raise QgistTypeError(tr('"config_group" is not a group of settings'))

        name = tr('Local QGIS C++ Plugin Repository')
        repo_id = f'{name:s} ({random.randint(2**31, 2**32 - 1):x})' # avoid collisions!

        return cls(
            repo_id = repo_id,
            name = name,
            active = True,
            protected = True,
            repository_type = cls.REPO_TYPE,
            plugin_releases = list(),
            config_group = config.get_group(CONFIG_GROUP_MANAGER_REPOS).get_group(repo_id),
            )
