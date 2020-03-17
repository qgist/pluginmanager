# -*- coding: utf-8 -*-

"""

QGIST PLUGIN MANAGER
QGIS Plugin for Managing QGIS Plugins
https://github.com/qgist/pluginmanager

    qgist/pluginmanager/dtype_version.py: Version data type

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
# CONST
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

VERSION_PREFIXES = (
    'VERSION', 'VER.', 'VER', 'V.', 'V',
    'REVISION', 'REV.', 'REV', 'R.', 'R'
    )

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# CLASS
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

class dtype_version_class:
    """
    Allows to represent and compare versions (of QGIS and plugins)
    """

    def __init__(self, *elements):
        pass

    def __repr__(self):
        return '<version>'

    def __eq__(self, other):
        return False
    def __ne__(self, other):
        return False
    def __lt__(self, other):
        return False
    def __le__(self, other):
        return False
    def __ge__(self, other):
        return False
    def __gt__(self, other):
        return False

    @staticmethod
    def _normalize_version_string(version_string):
        """ remove possible prefix from given string and convert to uppercase """

        if not isinstance(version_string, str):
            raise TypeError('version_string must be of type str')

        if len(version_string) == 0:
            return ''

        version_string = version_string.upper().strip(' \t\n')
        for prefix in VERSION_PREFIXES:
            if version_string.startswith(prefix):
                version_string = version_string[len(prefix):].strip(' \t\n')

        return version_string

    @classmethod
    def from_pluginversion(cls, plugin_version):

        return cls()

    @classmethod
    def from_qgisversion(cls, qgis_version):

        return cls()
