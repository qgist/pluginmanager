# -*- coding: utf-8 -*-

"""

QGIST PLUGIN MANAGER
QGIS Plugin for Managing QGIS Plugins
https://github.com/qgist/pluginmanager

    qgist/pluginmanager/metadata_spec.py: Meta data specification

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

from .dtype_version import dtype_version_class

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# PLUGIN META
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

METADATA_FIELD_DTYPES = (str, bool, dtype_version_class)

METADATA_FIELDS_SPEC = (
    {
        'comment': 'module name',
        'dtype': str,
        'name': 'id',
        'is_required': True,
    },
    {
        'comment': 'human readable plugin name',
        'dtype': str,
        'i18n': True,
        'name': 'name',
        'is_required': True,
    },
    {
        'comment': 'short description of the plugin purpose only',
        'dtype': str,
        'i18n': True,
        'name': 'description',
        'is_required': True,
    },
    {
        'comment': 'longer description: how does it work, where does it install, how to run it?',
        'dtype': str,
        'i18n': True,
        'name': 'about',
        'is_required': True,
    },
    {
        'comment': 'will be removed?',
        'dtype': str,
        'name': 'category',
    }, # TODO
    {
        'comment': 'comma separated, spaces allowed',
        'dtype': str,
        'i18n': True,
        'name': 'tags',
    },
    {
        'comment': 'may be multiline',
        'dtype': str,
        'name': 'changelog',
    },
    {
        'dtype': str,
        'name': 'author', # author_name
        'is_required': True,
    },
    {
        'dtype': str,
        'name': 'email', # author_email
        'is_required': True,
    },
    {
        'comment': 'url to the plugin homepage',
        'dtype': str,
        'name': 'homepage',
    },
    {
        'comment': 'url to a tracker site',
        'dtype': str,
        'name': 'tracker',
    },
    {
        'comment': 'url to the source code repository',
        'dtype': str,
        'name': 'repository', # 'code_repository'
        'is_required': True,
    },
    # {
    #     'comment': 'installed instance version',
    #     'dtype': str,
    #     'name': 'version_installed',
    # },
    # {
    #     'comment': 'absolute path to the installed library / Python module',
    #     'dtype': str,
    #     'name': 'library',
    # },
    {
        'comment': 'path to the first:(INSTALLED | AVAILABLE) icon',
        'dtype': str,
        'name': 'icon',
    },
    # {
    #     'comment': 'True if Python plugin',
    #     'dtype': bool,
    #     'default_value': True,
    #     'name': 'pythonic',
    # },
    # {
    #     'comment': 'True if core plugin',
    #     'dtype': bool,
    #     'name': 'readonly',
    # },
    # {
    #     'comment': 'True if installed',
    #     'dtype': bool,
    #     'name': 'installed',
    # },
    # {
    #     'comment': 'True if available in repositories',
    #     'dtype': bool,
    #     'name': 'available',
    # },
    # {
    #     'comment': '( not installed | new ) | ( installed | upgradeable | orphan | newer )',
    #     'dtype': str,
    #     'name': 'status',
    # }, # TODO
    # {
    #     'comment': 'NULL | broken | incompatible | dependent',
    #     'dtype': str,
    #     'name': 'error',
    # }, # TODO
    # {
    #     'comment': 'error description',
    #     'dtype': str,
    #     'name': 'error_details',
    # }, # TODO
    {
        'comment': 'true if experimental, false if stable',
        'dtype': bool,
        'name': 'experimental',
    },
    {
        'comment': 'true if deprecated, false if actual',
        'dtype': bool,
        'name': 'deprecated',
    },
    # {
    #     'comment': 'true if trusted, false if not trusted',
    #     'dtype': bool,
    #     'name': 'trusted',
    # }, # TODO
    # {
    #     'comment': 'available version',
    #     'dtype': str,
    #     'name': 'version_available',
    # },
    # {
    #     'comment': 'the remote repository id',
    #     'dtype': str,
    #     'name': 'zip_repository',
    # }, # TODO
    # {
    #     'comment': 'url for downloading the plugin',
    #     'dtype': str,
    #     'name': 'download_url',
    # },
    # {
    #     'comment': 'the zip file name to be unzipped after downloaded',
    #     'dtype': str,
    #     'name': 'filename',
    # },
    # {
    #     'comment': 'number of downloads',
    #     'dtype': str,
    #     'name': 'downloads',
    # },
    # {
    #     'comment': 'average vote',
    #     'dtype': str,
    #     'name': 'average_vote',
    # },
    # {
    #     'comment': 'number of votes',
    #     'dtype': str,
    #     'name': 'rating_votes',
    # },
    {
        'comment': 'PIP-style comma separated list of plugin dependencies',
        'dtype': str,
        'name': 'plugin_dependencies',
    },
    {
        'comment': 'dotted notation of minimum QGIS version',
        'dtype': dtype_version_class,
        'dtype_constructor': 'qgisversion',
        'dtype_constructor_kwargs': {'fix_plugin_compatibility': True}, # TODO is it actually True?
        'name': 'qgisMinimumVersion',
        'is_required': True,
    },
    {
        'comment': 'dotted notation of maximum QGIS version',
        'dtype': dtype_version_class,
        'dtype_constructor': 'from_qgisversion',
        'dtype_constructor_kwargs': {'fix_plugin_compatibility': False}, # TODO is it actually False?
        'name': 'qgisMaximumVersion',
    },
    {
        'dtype': dtype_version_class,
        'dtype_constructor': 'from_pluginversion',
        'name': 'version',
        'is_required': True,
    },
    {
        'comment': 'determines if the plugin provides processing algorithms',
        'dtype': bool,
        'name': 'hasProcessingProvider',
    },
    {
        'comment': 'determines if the plugin provides functionallity for server',
        'dtype': bool,
        'name': 'server',
    },
)
