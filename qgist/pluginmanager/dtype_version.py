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
    'REVISION', 'REV.', 'REV', 'R.', 'R',
    )

VERSION_SUFFIXES = (
    'ALPHA', 'BETA', 'PREVIEW', 'RC', 'TRUNK',
    )

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# CLASS
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

class dtype_version_class:
    """
    Allows to represent and compare versions (of QGIS and plugins)

    For compatibilty, this follows most logic of QGIS' `python/pyplugin_installer/version_compare.py`.
    """

    def __init__(self, *elements):

        for index, element in enumerate(elements):
            if not isinstance(element, str) and not isinstance(element, int):
                raise TypeError(f'parameter {index:d} is neither str nor int.')

        self._elements = elements

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
    def _normalize_version_str(version_str):
        """ remove possible prefix from given string and convert to uppercase """

        if not isinstance(version_str, str):
            raise TypeError('version_str must be of type str')

        if len(version_str) == 0:
            return ''

        version_str = version_str.upper().strip(' \t\n')
        for prefix in VERSION_PREFIXES:
            if version_str.startswith(prefix):
                version_str = version_str[len(prefix):].strip(' \t\n')

        return version_str

    @staticmethod
    def _split_version_str(version_str):
        """ convert string to list of numbers and words """

        if not isinstance(version_str, str):
            raise TypeError('version_str must be of type str')

        # return 0 for delimiter, 1 for digit and 2 for alphabetic character
        char_type = lambda char: 0 if char in ('.', '-', '_', ' ') else (1 if char.isdigit() else 2)

        elements = [version_str[0]]
        for index in range(1, len(version_str)):
            if char_type(version_str[index]) == 0:
                pass
            elif char_type(version_str[index]) == char_type(version_str[index - 1]):
                elements[-1] += version_str[index]
            else:
                elements.append(version_str[index])

        return elements

    @classmethod
    def from_pluginversion(cls, plugin_version_str):

        if not isinstance(plugin_version_str, str):
            raise TypeError('plugin_version_str must be of type str')

        return cls()

    @classmethod
    def from_qgisversion(cls, qgis_version_str):

        if not isinstance(qgis_version_str, str):
            raise TypeError('qgis_version_str must be of type str')

        return cls()
