# -*- coding: utf-8 -*-

"""

QGIST PLUGIN MANAGER
QGIS Plugin for Managing QGIS Plugins
https://github.com/qgist/pluginmanager

    qgist/pluginmanager/backends/qgis/dtype_pluginrelease.py: Plugin release data type

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

from .dtype_cache import dtype_cache_class

from ...const import REPO_BACKEND_QGISLEGACYPYTHON
from ...dtype_metadata import dtype_metadata_class
from ...dtype_pluginrelease_base import dtype_pluginrelease_base_class

from ....error import QgistValueError
from ....util import tr

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# CLASS
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

class dtype_pluginrelease_class(dtype_pluginrelease_base_class):

    _repo_type = REPO_BACKEND_QGISLEGACYPYTHON
    _cache = dtype_cache_class(_repo_type)

    # """
    # - Properties
    #     - Caches
    #     - Dependencies
    #         - inter-plugin
    #         - plugin to python packages (through source / other package manager)
    # """

    def _is_in_cache(self):

        if not self._meta['file_name'].value_set:
            raise QgistValueError(tr('"file_name" not set in meta data'))

        return self._meta['file_name'].value in self._cache

    def _fetch_from_remote_to_cache_file(self):

        if self._is_in_cache():
            return
        if not self._meta['download_url'].value_set:
            raise QgistValueError(tr('"download_url" not set in meta data'))

        self._cache.add_remote_file(
            filename = self._meta['file_name'].value,
            url = self._meta['download_url'].value,
            authcfg = None, # TODO
            )

    def _check_file_in_cache(self):

        if not self._is_in_cache():
            raise QgistValueError(tr('file is not in cache'))

        namelist = self._cache.get_file_entries(self._meta['file_name'].value)

        plugin_names = [name[:-1] for name in namelist if name.count('/') == 1 and name.endswith('/')]
        if len(plugin_names) == 0:
            raise QgistValueError(tr('There is no plugin in the zip-file (top-level directory missing)'))
        if len(plugin_names) > 1:
            raise QgistValueError(tr('There is more than one plugin in the zip-file (multiple top-level directories)'))

        plugin_name = plugin_names[0]
        if plugin_name != self._id:
            raise QgistValueError(tr('Plugin name mismatch'))

        if not f'{self._id:s}/__init__.py' in namelist:
            raise QgistValueError(tr('Plugin init file missing'))
        if not f'{self._id:s}/metadata.py' in namelist:
            raise QgistValueError(tr('Plugin metadata file missing'))

    def _update_metadata_from_cache_file(self):

        if not self._is_in_cache():
            raise QgistValueError(tr('file is not in cache'))

        new_meta_raw = self._cache.get_file_entry(
            filename = self._meta['file_name'].value,
            entryname = f'{self._id:s}/metadata.txt',
            password = None, # TODO
            )
        new_meta = dtype_metadata_class.from_metadatatxt(self._id, new_meta_raw)
        # TODO self._meta.update(new_meta)

    def _unpack_from_cache_file_to_tmp_fld(self):
        pass # TODO

    # is_python_plugin_dir is implemented in dtype_pluginrelease_base_class

    def _move_from_tmp_fld_to_install_fld(self):
        pass # TODO
