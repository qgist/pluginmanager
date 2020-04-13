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
from typing import Generator, Iterator

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# IMPORT (Internal)
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

from .metadata_spec import METADATA_FIELDS_SPEC
from .dtype_metadata_field import dtype_metadata_field_class
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

    def __init__(self, **import_fields):
        """
        `import_fields` is a dict of keys (field names, type `str`) and values (field values, all type `str`).
        """

        self._fields = {
            field['name']: dtype_metadata_field_class(**field) for field in METADATA_FIELDS_SPEC
            }

        for key in import_fields.keys():
            if import_fields[key] is None:
                continue
            if key not in self._fields.keys():
                self._fields[key] = dtype_metadata_field_class.from_unknown(key, import_fields[key])
            else:
                self._fields[key].value_string = import_fields[key] # Import of values of known fields and type cast happens here!

        self._id = self._fields['id'].value

    def __repr__(self):

        return f'<metadata id="{self._id:s}">'

    def __getitem__(self, name):

        if not isinstance(name, str):
            raise QgistTypeError(tr('"name" must be a str'))
        if name not in self._fields.keys():
            raise QgistMetaKeyError(tr('"name" is not a valid meta data field'))

        return self._fields[name]

    def keys(self):

        return (key for key in self._fields.keys())

    def required_fields_present(self, ignored_fields = None):
        "`email` is required but e.g. not exposed in plugins.xml from plugins.qgis.org - can be ignored"

        if ignored_fields is None:
            ignored_fields = tuple()

        if not any((isinstance(ignored_fields, dtype) for dtype in (Generator, Iterator, list, tuple))):
            raise QgistTypeError(tr('"ignored_fields" must be any of the following: list, tuple, generator, iterator.'))
        ignored_fields = tuple(ignored_fields)
        if not all((isinstance(field_id, str) for field_id in ignored_fields)):
            raise QgistTypeError(tr('All ignored field ids must be str.'))

        for field_id in self._fields.keys():
            if all((
                not self._fields[field_id].value_set,
                self._fields[field_id].is_required,
                field_id not in ignored_fields,
                )):
                return False

        return True

    def update(self, other):
        "Similar to dict.update, update this metadata with content from other metadata"

        if not isinstance(other, type(self)):
            raise QgistTypeError(tr('"other" is not meta data'))
        if self['id'].value != other['id'].value:
            raise QgistValueError(tr('id mismatch'))

        for key in other.keys():
            if key == 'id':
                continue
            if key not in self.keys():
                self._fields[key] = other[key].copy()
            else:
                self._fields[key].update(other[key])

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# EXPORT
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

    def as_config_decompressed(self):
        "Export meta data to uncompressed configuration data (JSON-serializable dict)"

        return {
            field_id: field.value_string
            for field_id, field in self._fields.items()
            if field.value_set
            }

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# PRE-CONSTRUCTOR
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

    @classmethod
    def from_config_decompressed(cls, config_decompressed):
        "From available releases cache in config"

        if not isinstance(config_decompressed, dict):
            raise QgistTypeError(tr('"config_decompressed" must be a dict.'))
        if not all((isinstance(key, str) for key in config_decompressed.keys())):
            raise QgistTypeError(tr('All keys in config_decompressed must be str'))

        return cls(**config_decompressed)

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

        for a, b in (
            ('qgis_minimum_version', 'qgisMinimumVersion'),
            ('qgis_maximum_version', 'qgisMaximumVersion'),
            ('author_name', 'author'),
            ):
            xml_dict[b] = xml_dict.pop(a)

        if 'id' not in xml_dict.keys():
            if 'file_name' not in xml_dict.keys():
                raise QgistMetaKeyError(tr('Neither "id" nor "file_name" in XML meta data - no way to determine plugin id'))
            if not xml_dict['file_name'].lower().endswith('.zip'):
                raise QgistValueError(tr('Unusual value for "file_name", does not end on ".zip"'))
            if xml_dict['version'] not in xml_dict['file_name']:
                raise QgistValueError(tr('Version is not part of "file_name"'))
            xml_dict['id'] = xml_dict['file_name'][:-1*(len('.zip') + len(xml_dict['version']) + len('-'))]

        return cls(**xml_dict)

    @classmethod
    def from_metadatatxt(cls, plugin_id, metadatatxt_string):
        "Parses a metadata.txt string and returns a meta data object"

        cp = ConfigParser(interpolation = None)

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
