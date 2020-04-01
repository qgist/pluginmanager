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
# CLASS: META DATA
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

class dtype_metadata_class:
    """
    Meta data of one single plugin
    """

    def __init__(self, **fields):

        self._id = '' # TODO plugin id

    def __repr__(self):

        return f'<metadata id="{self._id:s}">'

    @classmethod
    def from_xml(cls, xml_string):

        return cls()

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# CLASS: META DATA FIELD
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

class _dtype_metadata_field_class:

    def __init__(self, name, dtype, is_required, default_value = None):

        self._name = name
        self._dtype = dtype
        self._is_required = is_required
        self._default_value = default_value

    def __repr__(self):

        return (
            '<meta_field '
            f'name="{self._name:s}" dtype={self._dtype.__name__} '
            f'required={"yes" if self._is_required else "no"}'
            '>'
            )
