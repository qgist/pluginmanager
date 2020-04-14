# -*- coding: utf-8 -*-

"""

QGIST PLUGIN MANAGER
QGIS Plugin for Managing QGIS Plugins
https://github.com/qgist/pluginmanager

    qgist/qgis_api.py: Collects references to QGIS API in central location

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

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# IMPORT (Internal)
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

from .error import (
    QgistRequestError,
    QgistTypeError,
    QgistValueError,
    )
from .util import tr

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# IMPORT (External)
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

from PyQt5.QtCore import QUrl as _QUrl
from PyQt5.QtNetwork import (
    QNetworkRequest as _QNetworkRequest,
    QNetworkReply as _QNetworkReply,
    )

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# IMPORT (QGIS)
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

from qgis.core import (
    QgsApplication as _QgsApplication,
    QgsBlockingNetworkRequest as _QgsBlockingNetworkRequest,
    Qgis as _Qgis,
    QgsSettings as _QgsSettings,
    )

# TODO <HACK>
# remove this eventually - Plugin Manager should manage this on its own
from qgis.utils import (
    plugins as _plugins,
    _plugin_modules,
    _builtin_import,
    )
# TODO </HACK>

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# ROUTINES: MISC
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

def get_qgis_version():

    return _Qgis.version()

def get_qgis_settings(default):

    # TODO return default if qgis import fails
    return _QgsSettings()

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# ROUTINES: RUNTIME
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

# TODO <HACK>
# remove this eventually - Plugin Manager should manage this on its own
def get_plugin_modules():

    return _plugins

def get_plugin_module_names():

    return _plugin_modules

def get_builtin_import():

    return _builtin_import # builtins.__import__
# TODO </HACK>

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# ROUTINES: DIRECTORIES
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

def get_python_path():

    root_fld = (
        _QgsApplication.buildOutputPath()
        if _QgsApplication.isRunningFromBuildDir() else
        _QgsApplication.pkgDataPath()
        )

    return os.path.abspath(os.path.join(root_fld, 'python'))

def get_home_python_path():

    root_fld = _QgsApplication.qgisSettingsDirPath()

    if os.path.abspath(root_fld) == os.path.abspath(os.path.join(os.path.expanduser('~'), '.qgis3')):
        return os.path.abspath(os.path.join(os.path.expanduser('~'), '.qgis3', 'python'))

    return os.path.abspath(os.path.join(root_fld, 'python'))

def get_qgis_settings_dir_path():

    return _QgsApplication.qgisSettingsDirPath()

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# HTTP AND QGIS AUTH MANAGER
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

def request_data(url, authcfg = None, redirection_counter = 1, max_redirect = 4):

    if not isinstance(url, str):
        raise QgistTypeError(tr('"url" must be a str'))
    if not url.lower().startswith('http://') and not url.lower().startswith('https://'):
        raise QgistValueError(tr('"url" does not look like a URL'))
    if not isinstance(authcfg, str) and authcfg is not None:
        raise QgistTypeError(tr('"authcfg" must be a str or None'))
    if not isinstance(redirection_counter, int):
        raise QgistTypeError(tr('"redirection_counter" must be a int'))
    if redirection_counter < 1:
        raise QgistValueError(tr('"redirection_counter" must be greater than zero'))
    if not isinstance(max_redirect, int):
        raise QgistTypeError(tr('"max_redirect" must be a int'))
    if max_redirect < 1:
        raise QgistValueError(tr('"max_redirect" must be greater than zero'))
    if redirection_counter > max_redirect:
        raise QgistValueError(tr('Exceeding maximum redirects'))

    request_blocking = _QgsBlockingNetworkRequest()
    request = _QNetworkRequest(_QUrl(url))
    _autothenticate_request(request, authcfg)
    _ = request_blocking.get(request) # TODO blocking_error?
    reply = request_blocking.reply()
    reply_error = reply.error()

    if reply_error != _QNetworkReply.NoError:
        raise QgistRequestError(tr('Request failed') + ':\n\n' + reply.errorString())

    if reply.attribute(_QNetworkRequest.HttpStatusCodeAttribute) == 301: # HTTP 301

        redirection_url = reply.attribute(_QNetworkRequest.RedirectionTargetAttribute)
        if redirection_url.isRelative():
            redirection_url = reply.url().resolved(redirection_url)

        redirection_counter += 1
        if redirection_counter > max_redirect:
            raise QgistRequestError(tr('Too many redirections!'))

        return request_data(
            url = redirection_url, authcfg = authcfg,
            redirection_counter = redirection_counter, max_redirect = max_redirect,
            )

    try:
        content = bytes(reply.content())
        return content
    except Exception as e:
        raise QgistRequestError(tr('Unexpected error while processing content') + ':\n\n' + str(e))

def _autothenticate_request(request, authcfg):

    if authcfg is None:
        return
    if len(authcfg.strip()) == 0:
        return

    success_bool = _QgsApplication.authManager().updateNetworkRequest(request, authcfg.strip())
    if not success_bool:
        raise QgistRequestError(tr('Failed to authenticate request'))
