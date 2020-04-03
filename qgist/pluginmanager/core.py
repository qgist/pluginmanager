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
# IMPORT (External Dependencies)
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

from PyQt5.QtGui import (
    QIcon,
    )
from PyQt5.QtWidgets import (
    QAction,
    )

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# IMPORT (Internal)
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

from .const import (
    CONFIG_FN,
    IFACE_SPEC,
    PLUGIN_ICON_FN,
    )
from .dtype_index import dtype_index_class
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
    Qgist_ALL_Errors,
    )
from ..msg import msg_critical
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
            raise QgistTypeError(tr('"iface" must be a QGIS iface object'))
        if not isinstance(plugin_root_fld, str):
            raise QgistTypeError(tr('"plugin_root_fld" must be str'))
        if not os.path.exists(plugin_root_fld):
            raise QgistValueError(tr('"plugin_root_fld" must exists'))
        if not os.path.isdir(plugin_root_fld):
            raise QgistValueError(tr('"plugin_root_fld" must be a directory'))

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

        self._ui_dict['action_manage'] = QAction(tr('&Plugin &Manager'))
        self._ui_dict['action_manage'].setEnabled(False)
        self._ui_dict['action_manage'].setIcon(QIcon(os.path.join(
            self._plugin_root_fld, ICON_FLD, PLUGIN_ICON_FN
            )))

        pluginManagerMenuText = tr('Qgist Plugin &Manager')
        self._iface.addPluginToMenu(pluginManagerMenuText, self._ui_dict['action_manage'])
        self._ui_cleanup.append(
            lambda: self._iface.removePluginMenu(pluginManagerMenuText, self._ui_dict['action_manage'])
            )

        self._wait_for_mainwindow = True
        self._iface.initializationCompleted.connect(self._connect_ui)

    def _connect_ui(self):

        if not self._wait_for_mainwindow:
            return
        self._wait_for_mainwindow = False
        self._iface.initializationCompleted.disconnect(self._connect_ui)

        try:
            config = dtype_settings_class(config_class(os.path.join(get_config_path(), CONFIG_FN)))
            self._index = dtype_index_class(config = config)
        except Qgist_ALL_Errors as e:
            msg_critical(e, self._mainwindow)
            return

        self._iface.pindex = self._index # TODO HACK for debugging in console

        # self._ui_dict['action_manage'].triggered.connect(self._open_manager) # TODO
        self._ui_dict['action_manage'].setEnabled(True)

    def unload(self):
        """
        QGis Plugin Interface Routine
        """

        for cleanup_action in self._ui_cleanup:
            cleanup_action()
