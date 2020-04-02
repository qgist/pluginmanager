# -*- coding: utf-8 -*-

"""

QGIST PLUGIN MANAGER
QGIS Plugin for Managing QGIS Plugins
https://github.com/qgist/pluginmanager

    qgist/pluginmanager/dtype_metadata.py: Plugin meta data type

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

from configparser import ConfigParser
from collections import OrderedDict

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# IMPORT (Internal)
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

from .const import (
    METADATA_FIELD_DTYPES,
    METADATA_FIELDS_SPEC,
    )
from .dtype_settings import dtype_settings_class
from .error import (
    QgistMetaKeyError,
    QgistMetaRequirementError,
    QgistMetaTxtError,
    )

from ..error import (
    QgistTypeError,
    QgistValueError,
    )
from ..util import tr

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# CLASS: META DATA
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

class dtype_metadata_class:
    """
    Meta data of one single plugin

    Immutable.
    """

    def __init__(self, **fields):

        self._fields = {
            field['name']: _dtype_metadata_field_class(**field) for field in METADATA_FIELDS_SPEC
            }

        for key in fields.keys():
            if key not in self._fields.keys():
                self._fields[key] = _dtype_metadata_field_class.from_unknown(key, fields[key])
            else:
                self._fields[key].value = fields[key]

        # TODO "email" is required but e.g. not exposed in plugins.xml from plugins.qgis.org
        # for key in self._fields.keys():
        #     if self._fields[key].value is None and self._fields[key].is_required:
        #         raise QgistMetaRequirementError(tr('meta data field not present but required'))

        self._id = self._fields['id'].value

    def __repr__(self):

        return f'<metadata id="{self._id:s}">'

    def __getitem__(self, name):

        if not isinstance(name, str):
            raise QgistTypeError(tr('"name" must be a str'))
        if name not in self._fields.keys():
            raise QgistMetaKeyError(tr('"name" is not a valid meta data field'))

        return self._fields[name].value

    @classmethod
    def from_xmldict(cls, xml_dict):
        "Fixes an XML dict from xmltodict and returns a meta data object"

        if not isinstance(xml_dict, dict) and not isinstance(xml_dict, OrderedDict):
            raise QgistTypeError(tr('"name" must be a dict.'))

        xml_dict = dict(xml_dict) # gets rid of OrderedDict and copies dict!

        if not all((isinstance(key, str) for key in xml_dict.keys())):
            raise QgistTypeError(tr('All keys in xml_dict must be str'))
        if not all(((isinstance(value, str) or value is None) for value in xml_dict.values())):
            raise QgistTypeError(tr('All values in xml_dict must be str or None'))

        for key in ('name', 'plugin_id'):
            xml_dict[key] = xml_dict.pop(f'@{key:s}')

        if xml_dict['@version'] != xml_dict['version']:
            raise QgistValueError('One single plugin release has two versions')
        xml_dict.pop('@version')

        if 'id' not in xml_dict.keys():
            if 'file_name' not in xml_dict.keys():
                raise QgistMetaKeyError(tr('Neither "id" nor "file_name" in XML meta data - no way to determine plugin id'))
            if not xml_dict['file_name'].lower().endswith('.zip'):
                raise QgistValueError(tr('Unusual value for "file_name", does not end on ".zip"'))
            if xml_dict['version'] not in xml_dict['file_name']:
                raise QgistValueError(tr('Version is not part of "file_name"'))
            xml_dict['id'] = xml_dict['file_name'][:-1*(len('.zip') + len(xml_dict['version']) + len('..'))]

        return cls(**xml_dict)

    @classmethod
    def from_metadatatxt(cls, plugin_id, metadatatxt_string):
        "Parses a metadata.txt string and returns a meta data object"

        cp = ConfigParser()

        try:
            cp.read_string(metadatatxt_string)
        except Exception as e:
            raise QgistMetaTxtError(tr('failed to parse metadata.txt') + ': ' + str(e))

        try:
            general = cp['general']
        except Exception as e:
            raise QgistMetaTxtError(tr('failed to fetch section "general" from metadata.txt') + ': ' + str(e))

        try:
            fields = dict(general)
        except Exception as e:
            raise QgistMetaTxtError(tr('failed to convert section "general" from metadata.txt to dict') + ': ' + str(e))

        return cls(id = plugin_id, **fields)

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# CLASS: META DATA FIELD
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

class _dtype_metadata_field_class:
    """
    Represents one field of meta data

    Mutable, but not exposed beyond dtype_metadata_class, which is immutable.
    """

    def __init__(self,
        name, dtype,
        is_required = False, value = None, i18n = False, known = True,
        comment = '',
        ):

        if not isinstance(name, str):
            raise QgistTypeError(tr('"name" must be a str.'))
        if len(name) == 0:
            raise QgistValueError(tr('"name" must not be empty.'))
        if dtype not in METADATA_FIELD_DTYPES:
            raise QgistTypeError(tr('"dtype" unknown.'))
        if not isinstance(is_required, bool):
            raise QgistTypeError(tr('"is_required" must be a bool.'))
        if not isinstance(value, dtype) and value is not None:
            raise QgistTypeError(tr('"value" does not have matching type.'))
        if not isinstance(i18n, bool):
            raise QgistTypeError(tr('"i18n" must be a bool.'))
        if not isinstance(known, bool):
            raise QgistTypeError(tr('"known" must be a bool.'))
        if not isinstance(comment, str):
            raise QgistTypeError(tr('"comment" must be a str.'))

        self._name = name
        self._dtype = dtype
        self._is_required = is_required
        self._value = value
        self._i18n = i18n # TODO unused
        self._known = known # is meta field a known one?
        self._comment = comment # TODO unused

    def __repr__(self):

        return (
            '<meta_field '
            f'name="{self._name:s}" dtype={self._dtype.__name__} '
            f'known={"yes" if self._known else "no"} '
            f'i18n={"yes" if self._i18n else "no"} '
            f'required={"yes" if self._is_required else "no"}'
            '>'
            )

    @property
    def value(self):

        return self._value

    @value.setter
    def value(self, new_value):

        if not any((isinstance(new_value, dtype) for dtype in METADATA_FIELD_DTYPES)):
            raise QgistTypeError(tr('"new_value" does not have valid type'))

        if self._dtype == str:
            new_value = str(new_value)
        if self._dtype == bool:
            new_value = dtype_settings_class.str_to_bool(new_value)

        if not isinstance(new_value, self._dtype):
            raise QgistTypeError(tr('"new_value" was not converted to correct type'))

        self._value = new_value

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
