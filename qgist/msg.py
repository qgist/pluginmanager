# -*- coding: utf-8 -*-

"""

QGIST PLUGIN MANAGER
QGIS Plugin for Managing QGIS Plugins
https://github.com/qgist/pluginmanager

    qgist/msg.py: QGIST ui error messages

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

import traceback

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# IMPORT (External Dependencies)
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

from PyQt5.Qt import QWidget
from PyQt5.QtWidgets import QMessageBox

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# IMPORT (Internal)
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

from .error import QgistTypeError
from .util import tr

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# ROUTINES
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

def msg_critical(exception, widget = None):

    _msg('critical', tr('Critical error'), exception, widget)

def msg_warning(exception, widget = None):

    _msg('warning', tr('Warning'), exception, widget)

def _msg(msg_type, msg_title, exception, widget = None):

    if not isinstance(exception, Exception):
        raise QgistTypeError(tr('"exception" must be of type Exception'), 'msg')
    if not isinstance(widget, QWidget) and widget is not None:
        raise QgistTypeError(tr('"widget" must be of type QWidget or None'), 'msg')

    if len(exception.args) == 0:
        msg = tr('Internal error. No description can be provided. Please file a bug!')
    else:
        msg = str(exception.args[0])

    msg += '\n\n---------------------------\n\n' + traceback.format_exc()

    getattr(QMessageBox, msg_type)(
        widget,
        msg_title,
        msg,
        QMessageBox.Ok
        )
