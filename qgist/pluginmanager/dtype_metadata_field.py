# -*- coding: utf-8 -*-

"""

QGIST PLUGIN MANAGER
QGIS Plugin for Managing QGIS Plugins
https://github.com/qgist/pluginmanager

    qgist/pluginmanager/dtype_metadata_field.py: Plugin meta data field type

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
# IMPORT (Internal)
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

from .metadata_spec import METADATA_FIELD_DTYPES

from ..error import (
    QgistTypeError,
    QgistValueError,
    )
from ..util import tr

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# CLASS
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

class dtype_metadata_field_class:
    """
    Represents one field of meta data

    Mutable.
    """

    def __init__(self,
        name, dtype,
        value = None, default_value = None, importer = None, exporter = None,
        is_required = False, i18n = False, known = True,
        comment = '',
        ):

        if not isinstance(name, str):
            raise QgistTypeError(tr('"name" must be a str.'))
        if len(name) == 0:
            raise QgistValueError(tr('"name" must not be empty.'))
        if dtype not in METADATA_FIELD_DTYPES:
            raise QgistTypeError(tr('"dtype" unknown or broken.'))
        if not hasattr(importer, '__call__') and importer is not None:
            raise QgistTypeError(tr('"importer" must be callable or None.'))
        if not hasattr(exporter, '__call__') and exporter is not None:
            raise QgistTypeError(tr('"exporter" must be callable or None.'))
        if not isinstance(is_required, bool):
            raise QgistTypeError(tr('"is_required" must be a bool.'))
        if not isinstance(i18n, bool):
            raise QgistTypeError(tr('"i18n" must be a bool.'))
        if not isinstance(known, bool):
            raise QgistTypeError(tr('"known" must be a bool.'))
        if not isinstance(comment, str):
            raise QgistTypeError(tr('"comment" must be a str.'))

        self._name = name
        self._dtype = dtype
        self._importer = importer
        self._exporter = exporter
        self._is_required = is_required
        self._value = None
        self._known = known # is meta field a known one?

        self._i18n = i18n # TODO unused
        self._comment = comment # TODO unused

        if not self._is_valid_value(value) and value is not None:
            raise QgistTypeError(tr('"value" does not have matching tyspe.'))
        if not self._is_valid_value(default_value) and default_value is not None:
            raise QgistTypeError(tr('"default_value" does not have matching tyspe.'))

        self._value = value
        self._default_value = default_value

    def __repr__(self):

        return (
            '<meta_field '
            f'name="{self._name:s}" '
            f'dtype={getattr(self._dtype, "__name__", str(self._dtype)):s} '
            f'set={"yes" if self.value_set else "no"} '
            f'known={"yes" if self._known else "no"} '
            f'i18n={"yes" if self._i18n else "no"} '
            f'required={"yes" if self._is_required else "no"}'
            '>'
            )

    def _is_valid_value(self, value):

        return isinstance(value, self._dtype)

    def _value_to_string(self, value):

        if self._exporter is None:
            return str(value)

        value_str = self._exporter(value)
        if not isinstance(value_str, str):
            raise QgistTypeError(tr('"value_str" must be a str.'))
        return value_str

    @property
    def value_set(self):
        return self._value is not None

    @property
    def default_value_set(self):
        return self._default_value is not None

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):
        if not self._is_valid_value(new_value):
            raise QgistTypeError(tr('"new_value" does not have valid type'))
        self._value = new_value

    @property
    def default_value(self):
        return self._default_value

    @property
    def value_string(self):
        if not self.value_set:
            raise QgistValueError(tr('Nothing to export to string - value not set.'))
        return self._value_to_string(self._value)

    @value_string.setter
    def value_string(self, new_value_str):
        if not isinstance(new_value_str, str):
            raise QgistTypeError(tr('"new_value_str" must be a str.'))
        if self._importer is not None:
            new_value = self._importer(new_value_str)
        else:
            new_value = self._dtype(new_value_str)
        self.value = new_value

    @property
    def default_value_string(self):
        if not self.default_value_set:
            raise QgistValueError(tr('Nothing to export to string - default_value not set.'))
        return self._value_to_string(self._default_value)

    @property
    def is_required(self):
        return self._is_required

    @classmethod
    def from_unknown(cls, name, value):

        return cls(
            name = name,
            value = value,
            dtype = type(value),
            known = False,
            )
