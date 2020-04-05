# -*- coding: utf-8 -*-

"""

QGIST PLUGIN MANAGER
QGIS Plugin for Managing QGIS Plugins
https://github.com/qgist/pluginmanager

    qgist/pluginmanager/dtype_pluginrelease.py: Plugin release data type

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

import ast
import os

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# IMPORT (Internal)
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

from .error import QgistNotAPluginDirectoryError
from .dtype_metadata import dtype_metadata_class
from .dtype_settings import dtype_settings_class
from .dtype_version import dtype_version_class

from ..error import (
    QgistTypeError,
    QgistValueError,
    )
from ..util import tr

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# CLASS
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

class dtype_pluginrelease_base_class:
    """
    A release of a certain plugin, one version from one backend

    Mutable.
    """

    def __init__(self,
        plugin_id, version,
        has_processingprovider, has_serverfuncs, experimental, path,
        meta,
        ):

        if not isinstance(plugin_id, str):
            raise QgistTypeError(tr('"plugin_id" must be a str.'))
        if len(plugin_id) == 0:
            raise QgistValueError(tr('"plugin_id" must not be empty.'))
        if not isinstance(version, dtype_version_class):
            raise QgistTypeError(tr('"version" must be a version.'))
        if not isinstance(has_processingprovider, bool):
            raise QgistTypeError(tr('"has_processingprovider" must be a bool.'))
        if not isinstance(has_serverfuncs, bool):
            raise QgistTypeError(tr('"has_serverfuncs" must be a bool.'))
        if not isinstance(experimental, bool):
            raise QgistTypeError(tr('"experimental" must be a bool.'))
        if not isinstance(path, str) and path is not None:
            raise QgistTypeError(tr('"path" must be a str or None.'))
        if isinstance(path, str):
            if not os.path.isdir(path):
                raise QgistValueError(tr('If "path" is a str, it must exist'))
        if not isinstance(meta, dtype_metadata_class):
            raise QgistTypeError(tr('"meta" must be meta data.'))

        self._id = plugin_id
        self._version = version
        self._has_processingprovider = has_processingprovider
        self._has_serverfuncs = has_serverfuncs
        self._experimental = experimental
        self._path = path
        self._meta = meta

    def __repr__(self):

        return (
            '<plugin_release '
            f'id="{self._id:s}" '
            f'experimental={"yes" if self._experimental else "no":s} '
            f'processingprovider={"yes" if self.has_processingprovider else "no":s} '
            f'serverfuncs={"yes" if self.has_serverfuncs else "no":s}'
            '>'
            )

    def __eq__(self, other):

        return all((
            self.version == other.version,
            self.experimental == other.experimental,
            self.has_processingprovider == other.has_processingprovider,
            self.has_serverfuncs == other.has_serverfuncs,
            ))

    @property
    def id(self):
        return self._id

    @property
    def has_processingprovider(self):
        return self._has_processingprovider

    @property
    def has_serverfuncs(self):
        return self._has_serverfuncs

    @property
    def experimental(self):
        return self._experimental

    @property
    def version(self):
        return self._version

    @property
    def meta(self):
        return self._meta

    @property
    def path(self):
        return self._path

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# HELPER
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

    @staticmethod
    def is_python_plugin_dir(in_path):
        "Does a given folder contain a QGIS plugin?"

        if not os.path.isdir(in_path):
            return False
        if not os.path.isfile(os.path.join(in_path, '__init__.py')):
            return False
        if not os.path.isfile(os.path.join(in_path, 'metadata.txt')):
            return False

        return True

    @classmethod
    def fix_meta_by_setting_defaults(cls, meta):
        "Attempts to fix missing meta data fields by setting them to their defaults"

        if not meta['experimental'].value_set:
            meta['experimental'].value = meta['experimental'].default_value

    @classmethod
    def fix_meta_by_inspecting_plugindir(cls, meta, path):
        "Attempts to guess missing meta data fields by looking at plugin source code"

        if not isinstance(meta, dtype_metadata_class):
            raise QgistTypeError(tr('"meta" bust be meta data'))
        if not isinstance(path, str):
            raise QgistTypeError(tr('"path" must be str'))
        if not cls.is_python_plugin_dir(path):
            raise QgistNotAPluginDirectoryError(tr('"path" does not point to a plugin'))

        if not meta['server'].value_set:
            with open(os.path.join(path, '__init__.py'), 'r', encoding = 'utf-8') as f: # TODO encoding from file?
                init_raw = f.read()
            meta['server'].value = cls._is_func_present(init_raw, 'serverClassFactory')

        if not meta['hasProcessingProvider'].value_set:
            # TODO trace "QgsProcessingProvider" and "initProcessing" method in plugin folder
            # https://docs.qgis.org/testing/en/docs/pyqgis_developer_cookbook/processing.html
            meta['hasProcessingProvider'].value = meta['hasProcessingProvider'].default_value

    @staticmethod
    def _is_func_present(raw_src, func_name):
        "Is a given function present in raw Python source code?"

        tree = ast.parse(raw_src)

        # TODO catch more edge cases
        for branch in tree.body:
            if isinstance(branch, ast.FunctionDef):
                if getattr(branch, 'name', None) == func_name:
                    return True
            if isinstance(branch, ast.ImportFrom):
                for item in getattr(branch, 'names', tuple()):
                    if getattr(item, 'asname', None) is None and getattr(item, 'name', None) == func_name:
                        return True
                    if getattr(item, 'asname', None) == func_name:
                        return True
            if isinstance(branch, ast.Assign):
                for target in getattr(branch, 'targets', tuple()):
                    if getattr(target, 'id', None) == func_name:
                        return True

        return False

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# PRE-CONSTRUCTOR
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

    @classmethod
    def from_installed(cls, path, config):

        if not isinstance(path, str):
            raise QgistTypeError(tr('"path" must be str'))
        if not cls.is_python_plugin_dir(path):
            raise QgistNotAPluginDirectoryError(tr('"path" does not point to a plugin'))
        if not isinstance(config, dtype_settings_class):
            raise QgistTypeError(tr('"config" must be a "dtype_settings_class" object.'))

        with open(os.path.join(path, 'metadata.txt'), 'r', encoding = 'utf-8') as f: # TODO is this always UTF-8?
            meta_raw = f.read()

        plugin_id = os.path.basename(path)
        meta = dtype_metadata_class.from_metadatatxt(plugin_id, meta_raw)
        cls.fix_meta_by_inspecting_plugindir(meta, path)
        cls.fix_meta_by_setting_defaults(meta)

        return cls(
            plugin_id = meta['id'].value,
            version = meta['version'].value,
            has_processingprovider = meta['hasProcessingProvider'].value,
            has_serverfuncs = meta['server'].value,
            experimental = meta['experimental'].value,
            path = path,
            meta = meta,
            )
