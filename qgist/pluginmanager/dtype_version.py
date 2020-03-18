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
# IMPORT (Python Standard Library)
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

import re

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
VERSION_DELIMITERS = (
    '.', '-', '_', ' ', # TODO commas, i.e. `,`?
    )

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# CLASS
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

class dtype_version_class:
    """
    Allows to represent and compare versions (of QGIS and plugins)

    For compatibility, this follows most logic of QGIS' `python/pyplugin_installer/version_compare.py`.
    """

    def __init__(self, *elements, original = None):

        for index, element in enumerate(elements):
            if not isinstance(element, str):
                raise TypeError(f'parameter {index:d} is not a str')
        if not isinstance(original, str) and original is not None:
            raise TypeError(f'original is not a str and not None')

        self._elements = elements
        self._original = original if original is not None else '.'.join(elements)

    def __repr__(self):

        return f'<version {".".join(self._elements):s} ("{self._original:s}")>'

    def __len__(self):

        return len(self._elements)

    def __eq__(self, other):

        if not isinstance(other, type(self)):
            raise TypeError('other is not a version')

        if len(self) != len(other):
            return False

        return all((
            (a == b) for a, b in zip(self._elements, other._elements)
            ))

    def __ne__(self, other):

        return not self.__eq__(other)

    def __lt__(self, other):

        if self.__eq__(other):
            return False

        return self._greater_than(other, self)

    def __gt__(self, other):

        if self.__eq__(other):
            return False

        return self._greater_than(self, other)

    def __le__(self, other):

        if self.__eq__(other):
            return True

        return self.__lt__(other)

    def __ge__(self, other):

        if self.__eq__(other):
            return True

        return self.__gt__(other)

    @classmethod
    def _greater_than(cls, a, b):
        "Compare two *unequal* versions a and b: Is a greater then b?"

        if not isinstance(a, cls):
            raise TypeError('a is not a version')
        if not isinstance(b, cls):
            raise TypeError('b is not a version')

        # set the shorter string as a base length
        base_len = len(a) if len(a) < len(b) else len(b)

        # try to determine within the common/base length
        for index in range(base_len):
            relation = cls._compare_elements(a[index], b[index])
            if relation != 0:
                return relation == 1

        # if the lists are identical till the end of the shorther string, try to compare the odd tail
        # with the simple space (because the 'alpha', 'beta', 'preview' and 'rc' are LESS then nothing)
        if len(a) > base_len:
            return cls._compare_elements(a[base_len], ' ') == 1
        if len(b) > base_len:
            return cls._compare_elements(' ', b[base_len]) == 1

        # if everything else fails, compare original strings
        return a._original > b._original

    @classmethod
    def _compare_elements(cls, x, y):
        "Compare version element x with version element y (0/==, 1/>, 2/<)"

        if not isinstance(x, str):
            raise TypeError('x is not a str')
        if not isinstance(y, str):
            raise TypeError('y is not a str')

        if x == y:
            return 0

        is_numeric = lambda element: len(element) > 0 and element.isnumeric() and element[0] != '0'
        rank_string = lambda element: 'Z' + element if element not in VERSION_SUFFIXES else element

        # try to compare as numeric values (but only if the first character is not 0):
        if is_numeric(x) and is_numeric(y):
            if int(x) == int(y):
                return 0
            elif int(x) > int(y):
                return 1
            else:
                return 2

        # if the strings aren't numeric or start from 0, compare them as a strings:
        # but first, set ALPHA < BETA < PREVIEW < RC < TRUNK < [NOTHING] < [ANYTHING_ELSE]
        return 1 if rank_string(x) > rank_string(y) else 2

    @staticmethod
    def _normalize_version_str(version_str):
        "Remove possible prefix from given string and convert to uppercase"

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
        "Convert string to list of numbers and words"

        if not isinstance(version_str, str):
            raise TypeError('version_str must be of type str')

        # return 0 for delimiter, 1 for digit and 2 for alphabetic character
        char_type = lambda char: 0 if char in VERSION_DELIMITERS else (1 if char.isdigit() else 2)

        elements = [version_str[0]]
        for index in range(1, len(version_str)):
            if char_type(version_str[index]) == 0:
                pass
            elif char_type(version_str[index]) == char_type(version_str[index - 1]):
                elements[-1] += version_str[index]
            else:
                elements.append(version_str[index])

        for element in elements:
            if len(element) == 0:
                raise ValueError('splitting elements failed, element of zero-length')

        return elements

    @classmethod
    def from_pluginversion(cls, plugin_version_str):
        "Parse plugin version string and return version object"

        if not isinstance(plugin_version_str, str):
            raise TypeError('plugin_version_str must be of type str')

        plugin_version = cls._split_version_str(
            cls._normalize_version_str(plugin_version_str)
            )

        return cls(*plugin_version, original = plugin_version_str)

    @classmethod
    def from_qgisversion(cls, qgis_version_str):
        "Parse QGIS version string and return version object"

        if not isinstance(qgis_version_str, str):
            raise TypeError('qgis_version_str must be of type str')

        x, y, z = re.findall(r'^(\d*).(\d*).(\d*)', qgis_version_str)[0]

        # Return current QGIS version number as X.Y.Z for testing plugin compatibility.
        # If Y = 99, bump up to (X+1.0.0), so e.g. 2.99 becomes 3.0.0
        # This way QGIS X.99 is only compatible with plugins for the upcoming major release.
        if y == '99':
            x = str(int(x) + 1)
            y = z = '0'

        return cls(x, y, z, original = qgis_version_str)
