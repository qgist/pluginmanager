# -*- coding: utf-8 -*-

"""

QGIST PLUGIN MANAGER
QGIS Plugin for Managing QGIS Plugins
https://github.com/qgist/pluginmanager

    qgist/pluginmanager/core.py: QGIST pluginmanager core

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

import os
import platform

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# IMPORT (Internal)
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

from .const import (
    CONFIG_FN,
    IFACE_SPEC,
    )
from .dtype_settings import dtype_settings_class
from .typechecking import conforms_to_spec

from ..const import (
    ICON_FLD,
    TRANSLATION_FLD,
    )
from ..config import (
    config_class,
    get_config_path,
    )
from ..error import (
    QgistTypeError,
    QgistValueError,
    )
from ..util import (
    tr,
    setupTranslation,
    )

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# CLASS: PLUGIN MANAGER CORE
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

class pluginmanager:
    """
    Core class
    """

    def __init__(self, iface, plugin_root_fld):

        if not conforms_to_spec(iface, IFACE_SPEC):
            raise QgistTypeError(tr('"iface" must be a QGIS iface object'), self)
        if not isinstance(plugin_root_fld, str):
            raise QgistTypeError(tr('"plugin_root_fld" must be str'), self)
        if not os.path.exists(plugin_root_fld):
            raise QgistValueError(tr('"plugin_root_fld" must exists'), self)
        if not os.path.isdir(plugin_root_fld):
            raise QgistValueError(tr('"plugin_root_fld" must be a directory'), self)

        self._iface = iface
        self._plugin_root_fld = plugin_root_fld

        self._mainwindow = self._iface.mainWindow()
        self._system = platform.system()

    def initGui(self):
        """
        QGis Plugin Interface Routine
        """

        self._translator, self._translator_path = setupTranslation(os.path.join(
            self._plugin_root_fld, TRANSLATION_FLD
            ))

        self._ui_dict = {}
        self._ui_cleanup = []

        # TODO self._init_ui()
        # TODO self._connect_ui()

        self._config = dtype_settings_class(config_class(os.path.join(get_config_path(), CONFIG_FN))) # TODO move ...

    def unload(self):
        """
        QGis Plugin Interface Routine
        """

        for cleanup_action in self._ui_cleanup:
            cleanup_action()
