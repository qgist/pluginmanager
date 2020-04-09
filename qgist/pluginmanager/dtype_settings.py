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
# IMPORT (Python Standard Library)
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

import base64
import json
import zlib

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# IMPORT (External Dependencies)
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

from PyQt5.QtCore import QDate

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# IMPORT (Internal)
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

from .const import CONFIG_DELIMITER
from ..config import config_class
from ..error import (
    QgistTypeError,
    QgistValueError,
    )
from ..util import tr

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# CLASS: SETTINGS MAIN
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
            raise QgistTypeError(tr('config must be an instance of config_class'))
        if not isinstance(try_qgis_settings, bool):
            raise QgistTypeError(tr('try_qgis_settings must be a bool'))

        self._config = config
        self._settings = None

        if not try_qgis_settings:
            return

        try:
            from qgis.core import QgsSettings
        except ModuleNotFoundError:
            QgsSettings = None
        self._settings = QgsSettings() if QgsSettings is not None else None

    def __repr__(self):

        return f'<settings ({id(self):x})>'

    def __getitem__(self, name):

        if not isinstance(name, str):
            raise QgistTypeError(tr('name is not str'))
        if len(name) == 0:
            raise QgistValueError(tr('name must not be empty'))

        setting = self._settings.value(name) if self._settings is not None else None

        if setting is None:
            return self._config[name]
        return self._convert_qt_to_python(setting)

    def __setitem__(self, name, value):

        if not isinstance(name, str):
            raise QgistTypeError(tr('name is not str'))
        if len(name) == 0:
            raise QgistValueError(tr('name must not be empty'))

        self._config[name] = value # does internal validity and type checks on value etc

        self._settings.setValue(name, value)

    def get(self, name, default):
        "dict get"

        if not isinstance(name, str):
            raise QgistTypeError(tr('name is not str'))
        if len(name) == 0:
            raise QgistValueError(tr('name must not be empty'))

        setting = self._settings.value(name) if self._settings is not None else None

        if setting is None:
            return self._config.get(name, default)
        return self._convert_qt_to_python(setting)

    def get_group(self, root):
        "get group by root"

        if not isinstance(root, str):
            raise QgistTypeError(tr('root is not str'))
        if len(root) == 0:
            raise QgistValueError(tr('root must not be empty'))

        return dtype_settings_group_class(self, root)

    def keys(self):
        "dict keys generator"

        keys = self._settings.allKeys() if self._settings is not None else None

        if keys is not None:
            return (key for key in keys) # keys is a list, should be a generator/iterator
        return self._config.keys()

    def keys_root(self):
        "dict keys generator - at root"

        return (item for item in set((
            key.split(CONFIG_DELIMITER, 1)[0]
            for key in self.keys()
            )))

    @staticmethod
    def _convert_qt_to_python(data):

        if config_class.check_value(data): # valid Python/JSON data type
            return data

        if isinstance(data, QDate):
            return data.toPyDate().isoformat() # returns date-time iso string

        raise QgistTypeError(tr('unknown data type from QGIS settings'))

    @staticmethod
    def str_to_bool(value):

        if not isinstance(value, str):
            raise QgistTypeError(tr('value is not str'))

        if value.lower() in ('yes', 'true', '1'):
            return True
        if value.lower() in ('no', 'false', '0'):
            return False

        # TODO inspired by https://github.com/3liz/QuickOSM/commit/ef5df529b841362d796574b62d78e12a5d929290
        if any((value.lower().startswith(item) for item in ('yes', 'true'))):
            return True
        if any((value.lower().startswith(item) for item in ('no', 'false'))):
            return False

        raise QgistValueError(tr('value can not be converted to bool'), value)

    @staticmethod
    def bool_to_str(value, style):

        styles = {
            'TrueFalse': lambda x: 'True' if x else 'False',
            'truefalse': lambda x: 'true' if x else 'false',
            'YesNo': lambda x: 'Yes' if x else 'No',
            'yesno': lambda x: 'yes' if x else 'no',
            '10': lambda x: '1' if x else '0',
            }

        if not isinstance(value, bool):
            raise QgistTypeError(tr('"value" must be a bool'))
        if not isinstance(style, str):
            raise QgistTypeError(tr('"style" must be a str'))
        if style not in styles.keys():
            raise QgistTypeError(tr('"style" is unknown'))

        return styles[style](value)

    @staticmethod
    def load(data):
        """
        Converts compressed configuration data back to Python objects
        """

        PACKING_VERSION = 'REPO_V001' # Making this future-proofed!

        if not isinstance(data, str):
            raise QgistTypeError(tr('data must be a str'))
        if not data.startswith(PACKING_VERSION):
            raise QgistValueError(tr('data must be packed configuration'))

        length_raw = data[len(PACKING_VERSION):(len(PACKING_VERSION) + 16)]
        if not length_raw.isnumeric():
            raise QgistValueError(tr('data does not have numeric length field - broken'))

        length = int(length_raw)
        data_raw = data[(len(PACKING_VERSION) + 16):]
        if length != len(data_raw):
            raise QgistValueError(tr('length information in data does not match actual length'))

        return json.loads(
            zlib.decompress(
                base64.b64decode(
                    data_raw.encode('utf-8') # to bytes (BASE64)
                    ) # to bytes (regular)
                ).decode('utf-8') # to decompressed, to string
            ) # to Python

    @staticmethod
    def dump(data):
        """
        Accepts anything that can be handled by JSON.
        Compresses data and prepares string which can be stored in configuration.
        """

        PACKING_VERSION = 'REPO_V001' # Making this future-proofed!

        if not config_class.check_value(data):
            raise QgistTypeError(tr('"value" contains not allowed types.'))

        packed = base64.b64encode(
            zlib.compress(
                json.dumps(data).encode('utf-8') # to JSON, to bytes
                ) # to compressed bytes
            ).decode('utf-8') # to base64, to string

        return f'{PACKING_VERSION:s}{len(packed):016d}{packed:s}'

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# CLASS: SETTINGS GROUP
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

class dtype_settings_group_class:
    """
    Mimics QgsSettings.beginGroup & QgsSettings.endGroup

    QgsSettings objects are finite state machines. The settings_group_class enables
    the settings_class to just work without the change of any state.

    Mutable.
    """

    def __init__(self, settings, root):

        if not isinstance(settings, dtype_settings_class):
            raise QgistTypeError(tr('settings must be an instance of config_class'))
        if not isinstance(root, str):
            raise QgistTypeError(tr('root must be a str'))
        if len(root) == 0:
            raise QgistValueError(tr('root must not be empty'))

        self._settings = settings
        self._root = root
        self._base = self._root + CONFIG_DELIMITER
        self._base_len = len(self._base)

    def __repr__(self):

        return f'<settings group (attached to {id(self._settings):x}, root "{self._root:s}")>'

    def __getitem__(self, name):

        if not isinstance(name, str):
            raise QgistTypeError(tr('name is not str'))
        if len(name) == 0:
            raise QgistValueError(tr('name must not be empty'))

        return self._settings[self._base + name]

    def __setitem__(self, name, value):

        if not isinstance(name, str):
            raise QgistTypeError(tr('name is not str'))
        if len(name) == 0:
            raise QgistValueError(tr('name must not be empty'))

        self._settings[self._base + name] = value

    @property
    def root(self):
        return self._root

    @property
    def settings(self):
        return self._settings

    def get(self, name, default):
        "dict get"

        if not isinstance(name, str):
            raise QgistTypeError(tr('name is not str'))
        if len(name) == 0:
            raise QgistValueError(tr('name must not be empty'))

        return self._settings.get(self._base + name, default)

    def get_group(self, root):
        "get group by root"

        if not isinstance(root, str):
            raise QgistTypeError(tr('root is not str'))
        if len(root) == 0:
            raise QgistValueError(tr('root must not be empty'))

        return type(self)(self._settings, self._base + root)

    def keys(self):
        "dict keys generator"

        return (item for item in set((
            key[self._base_len:]
            for key in self._settings.keys()
            if key.startswith(self._base) and len(key) > self._base_len
            )))

    def keys_root(self):
        "dict keys generator - at root"

        return (item for item in set((
            key[self._base_len:].split(CONFIG_DELIMITER, 1)[0]
            for key in self._settings.keys()
            if key.startswith(self._base) and len(key) > self._base_len
            )))
