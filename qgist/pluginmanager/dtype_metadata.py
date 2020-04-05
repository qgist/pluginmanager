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

from .metadata_spec import (
    METADATA_FIELD_DTYPES,
    METADATA_FIELDS_SPEC,
    )
from .dtype_settings import dtype_settings_class
from .dtype_version import dtype_version_class
from .error import (
    QgistMetaKeyError,
    # QgistMetaRequirementError, # TODO, see constructor below
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

    Mutable.
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
