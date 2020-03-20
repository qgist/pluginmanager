# -*- coding: utf-8 -*-

"""

QGIST PLUGIN MANAGER
QGIS Plugin for Managing QGIS Plugins
https://github.com/qgist/pluginmanager

    qgist/pluginmanager/dtype_settings.py: Settings data type

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

from ..config import config_class

from ..error import QgistTypeError

from ..util import tr

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# CLASS
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

class dtype_settings_class:
    """
    Transparent wrapper around QgsSettings - so it can be exchanged (for testing etc)
    Class enables redundant storage of settings: Into QgsSettings *and* config_class.
    When read, data from QgsSettings is preferred.

    Mutable.
    """

    def __init__(self, config, try_qgis_settings = True):

        if not isinstance(config, config_class):
            raise QgistTypeError(tr('config must be an instance of config_class'), self)
        if not isinstance(try_qgis_settings, bool):
            raise QgistTypeError(tr('try_qgis_settings must be a bool'), self)

        self._config = config

        self._qgis_settings = None
        if try_qgis_settings:
            self._load_qgis_settings()

    def _load_qgis_settings(self):

        try:
            from qgis.core import QgsSettings
        except ModuleNotFoundError:
            QgsSettings = None

        self._settings = QgsSettings() if QgsSettings is not None else None

    def __getitem__(self, name):

        return self._config[name]

    def __setitem__(self, name, value):

        self._config[name] = value

    def get(self, name, default):

        return self._config.get(name, default)
