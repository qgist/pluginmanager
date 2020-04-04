# -*- coding: utf-8 -*-

"""

QGIST PLUGIN MANAGER
QGIS Plugin for Managing QGIS Plugins
https://github.com/qgist/pluginmanager

    qgist/pluginmanager/const.py: Plugin constants

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
# MISC
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

CONFIG_FN = 'pluginmanager.json'
PLUGIN_ICON_FN = 'pluginmanager.svg'
PLUGIN_NAME = 'QgistPluginManager'

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# TYPE SPECS
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

CONFIG_DELIMITER = '/'

CONFIG_KEY_ALLOW_DEPRECATED = 'app/plugin_installer/allowDeprecated' # TODO
CONFIG_KEY_ALLOW_EXPERIMENTAL = 'app/plugin_installer/allowExperimental' # TODO

CONFIG_GROUP_MANAGER_REPOS = 'app/pluginmanager/repositories' # TODO
CONFIG_GROUP_QGISLEGACY_REPOS = 'app/plugin_repositories' # TODO

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# TYPE SPECS
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

IFACE_SPEC = {
    'typename': 'QgisInterface',
    'attrs': [
        'mainWindow',
        ]
    }

QGSSETTINGS_SPEC = {
    'typename': 'sip.wrappertype',
    'name': 'QgsSettings',
    'attrs': [
        'value',
        'setValue',
        ]
    }

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# REPO META
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

REPO_DEFAULT_URL = 'https://plugins.qgis.org/plugins/plugins.xml'
REPO_BACKEND_QGISLEGACYPYTHON = 'qgis'
REPO_BACKEND_QGISLEGACYCPP = 'cpp'

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# VERSIONS
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

VERSION_PREFIXES = (
    'VERSION', 'VER.', 'VER', 'V.', 'V',
    'REVISION', 'REV.', 'REV', 'R.', 'R',
    )
VERSION_UNSTABLE_SUFFIXES = (
    'ALPHA', 'BETA', 'PREVIEW', 'RC', 'TRUNK',
    )
VERSION_DELIMITERS = (
    '.', '-', '_', ' ', # TODO commas, i.e. `,`?
    )
