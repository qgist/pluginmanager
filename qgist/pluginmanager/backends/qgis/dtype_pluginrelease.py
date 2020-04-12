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

from ...const import REPO_BACKEND_QGISLEGACYPYTHON
from ...dtype_pluginrelease_base import dtype_pluginrelease_base_class

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# CLASS
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

class dtype_pluginrelease_class(dtype_pluginrelease_base_class):

    _repo_type = REPO_BACKEND_QGISLEGACYPYTHON

    # """
    # - Properties
    #     - Caches
    #     - Dependencies
    #         - inter-plugin
    #         - plugin to python packages (through source / other package manager)
    # """

    def _is_in_cache(self):
        return False # TODO

    def _fetch_from_remote_to_cache_file(self):
        pass # TODO

    def _read_metadata_from_cache_file(self):
        pass # TODO

    def _unpack_from_cache_file_to_tmp_fld(self):
        pass # TODO

    # is_python_plugin_dir is implemented in dtype_pluginrelease_base_class

    def _move_from_tmp_fld_to_install_fld(self):
        pass # TODO
