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

    def __init__(self,
        name, dtype,
        is_required = False, default_value = None, i18n = False,
        comment = "",
        ):

        self._name = name
        self._dtype = dtype
        self._is_required = is_required
        self._default_value = default_value
        self._i18n = i18n
        self._comment = comment

    def __repr__(self):

        return (
            '<meta_field '
            f'name="{self._name:s}" dtype={self._dtype.__name__} '
            f'i18n={"yes" if self._i18n else "no"} '
            f'required={"yes" if self._is_required else "no"}'
            '>'
            )

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# LIST OF FIELDS
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

_fields_spec = (
    {
        'comment': 'module name',
        'dtype': 'unicode',
        'name': 'id',
    },
    {
        'comment': 'human readable plugin name',
        'dtype': 'unicode',
        'name': 'name',
    },
    {
        'comment': 'short description of the plugin purpose only',
        'dtype': 'unicode',
        'name': 'description',
    },
    {
        'comment': 'longer description: how does it work, where does it install, how to run it?',
        'dtype': 'unicode',
        'name': 'about',
    },
    {
        'comment': 'will be removed?',
        'dtype': 'unicode',
        'name': 'category',
    },
    {
        'comment': 'comma separated, spaces allowed',
        'dtype': 'unicode',
        'name': 'tags',
    },
    {
        'comment': 'may be multiline',
        'dtype': 'unicode',
        'name': 'changelog',
    },
    {
        'comment': 'author name',
        'dtype': 'unicode',
        'name': 'author_name',
    },
    {
        'comment': 'author email',
        'dtype': 'unicode',
        'name': 'author_email',
    },
    {
        'comment': 'url to the plugin homepage',
        'dtype': 'unicode',
        'name': 'homepage',
    },
    {
        'comment': 'url to a tracker site',
        'dtype': 'unicode',
        'name': 'tracker',
    },
    {
        'comment': 'url to the source code repository',
        'dtype': 'unicode',
        'name': 'code_repository',
    },
    {
        'comment': 'installed instance version',
        'dtype': 'unicode',
        'name': 'version_installed',
    },
    {
        'comment': 'absolute path to the installed library / Python module',
        'dtype': 'unicode',
        'name': 'library',
    },
    {
        'comment': 'path to the first:(INSTALLED | AVAILABLE) icon',
        'dtype': 'unicode',
        'name': 'icon',
    },
    {
        'comment': 'True if Python plugin',
        'dtype': 'const bool=True',
        'name': 'pythonic',
    },
    {
        'comment': 'True if core plugin',
        'dtype': 'boolean',
        'name': 'readonly',
    },
    {
        'comment': 'True if installed',
        'dtype': 'boolean',
        'name': 'installed',
    },
    {
        'comment': 'True if available in repositories',
        'dtype': 'boolean',
        'name': 'available',
    },
    {
        'comment': '( not installed | new ) | ( installed | upgradeable | orphan | newer )',
        'dtype': 'unicode',
        'name': 'status',
    },
    {
        'comment': 'NULL | broken | incompatible | dependent',
        'dtype': 'unicode',
        'name': 'error',
    },
    {
        'comment': 'error description',
        'dtype': 'unicode',
        'name': 'error_details',
    },
    {
        'comment': 'true if experimental, false if stable',
        'dtype': 'boolean',
        'name': 'experimental',
    },
    {
        'comment': 'true if deprecated, false if actual',
        'dtype': 'boolean',
        'name': 'deprecated',
    },
    {
        'comment': 'true if trusted, false if not trusted',
        'dtype': 'boolean',
        'name': 'trusted',
    },
    {
        'comment': 'available version',
        'dtype': 'unicode',
        'name': 'version_available',
    },
    {
        'comment': 'the remote repository id',
        'dtype': 'unicode',
        'name': 'zip_repository',
    },
    {
        'comment': 'url for downloading the plugin',
        'dtype': 'unicode',
        'name': 'download_url',
    },
    {
        'comment': 'the zip file name to be unzipped after downloaded',
        'dtype': 'unicode',
        'name': 'filename',
    },
    {
        'comment': 'number of downloads',
        'dtype': 'unicode',
        'name': 'downloads',
    },
    {
        'comment': 'average vote',
        'dtype': 'unicode',
        'name': 'average_vote',
    },
    {
        'comment': 'number of votes',
        'dtype': 'unicode',
        'name': 'rating_votes',
    },
    {
        'comment': 'PIP-style comma separated list of plugin dependencies',
        'dtype': 'unicode',
        'name': 'plugin_dependencies',
    },
)

_fields = tuple([_dtype_metadata_field_class(**field) for field in _fields_spec])
