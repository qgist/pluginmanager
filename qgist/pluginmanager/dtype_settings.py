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
# IMPORT (External Dependencies)
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

from PyQt5.QtCore import QDate

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
    When written, data goes first into config_class, second into QgsSettings.

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

        setting = self._settings.value() if self._settings is not None else None

        if setting is None:
            return self._config[name]
        return self._convert_qt_to_python(setting)

    def __setitem__(self, name, value):

        self._config[name] = value # does internal type checks

        self._settings.setValue(name, value)

    def get(self, name, default):

        setting = self._settings.value() if self._settings is not None else None

        if setting is None:
            return self._config.get(name, default)
        return self._convert_qt_to_python(setting)

    def keys(self):

        keys = self._settings.allKeys() if self._settings is not None else None

        if keys is not None:
            return (key for key in keys) # keys is a list, should be a generator/iterator
        return self._config.keys()

    @staticmethod
    def _convert_qt_to_python(data):

        if config_class.check_value(data): # valid Python/JSON data type
            return data

        if isinstance(data, QDate)
            return data.toPyDate().isoformat() # returns date-time iso string

        raise QgistTypeError(tr('unknown data type from QGIS settings'), 'settings')
