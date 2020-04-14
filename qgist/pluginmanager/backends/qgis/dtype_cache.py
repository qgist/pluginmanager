# -*- coding: utf-8 -*-

"""

QGIST PLUGIN MANAGER
QGIS Plugin for Managing QGIS Plugins
https://github.com/qgist/pluginmanager

    qgist/pluginmanager/backends/qgis/dtype_cache.py: Plugin release local cache

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

import glob
import hashlib
import os
import zipfile

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# IMPORT (Internal)
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

from .abc import cache_abc

from ...const import REPO_CACHE_FLD

from ....config import get_config_path
from ....error import (
    QgistTypeError,
    QgistValueError,
    )
from ....qgis_api import request_data
from ....util import tr

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# CLASS
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

class dtype_cache_class(cache_abc):
    """
    Cache for holding (and managing) plugin ZIP-files locally

    Mutable.
    """

    def __init__(self, prefix):

        if not isinstance(prefix, str):
            raise QgistTypeError(tr('"prefix" must be a str'))
        if len(prefix) == 0:
            raise QgistValueError(tr('"prefix" must not be empty'))

        path = os.path.join(get_config_path(), REPO_CACHE_FLD, prefix)
        self._ensure_path(path)

        self._path = path
        self._files = {}
        self._refresh()

    def __repr__(self):

        return f'<cache files={len(self):d}>'

    def __len__(self):

        return len(self._files)

    def __getitem__(self, filename):
        "Translates filename to full path if filename is present in cache"

        self._check_filename(filename)
        if filename not in self:
            raise QgistValueError(tr('"filename" is not present in cache'))

        return self._files[filename]

    def __contains__(self, filename):
        "Checks if filename is present in cache"

        return filename in self._files.keys()

    @property
    def files(self):
        "Returns iterator of cached filenames (not their paths)"

        return (fn for fn in self._files.keys())

    @staticmethod
    def _check_filename(filename):
        "Raises exception if filename is not a valid zip-file name"

        if not isinstance(filename, str):
            raise QgistTypeError(tr('"filename" must be a str'))
        if len(filename) == 0:
            raise QgistValueError(tr('"filename" must not be empty'))
        if not filename.lower().endswith('.zip'):
            raise QgistValueError(tr('"filename" does not refer to a ZIP-file'))

    @staticmethod
    def _ensure_path(path):
        "Ensures that a path to a directory is actually present and writable"

        if os.path.exists(path) and not os.path.isdir(path):
            raise QgistValueError(tr('path points to existing path which is not a directory'))
        if not os.path.exists(path):
            try:
                os.makedirs(path, exist_ok = True)
            except Exception as e:
                raise QgistValueError(tr('path was not present, creation failed'), e)
        if not os.access(path, os.W_OK | os.R_OK):
            raise QgistValueError(tr('path is not writeable and/or readable'))

    @staticmethod
    def _get_cache_subdirs(filename):
        "Translates filename to cache sub-directories, i.e. its location in cache"

        filename_hash = hashlib.sha256(filename.encode('utf-8')).hexdigest()
        return filename_hash[:2], filename_hash[2:4]

    def _refresh(self):
        "Refreshes, i.e. rebuilds, the _files dict mapping filenames to absolute paths"

        new_files = {
            os.path.basename(path): path
            for path in glob.iglob(self._path + '/**', recursive = True)
            if path.lower().endswith('.zip') and os.path.isfile(path)
            }

        self._files.clear()
        self._files.update(new_files)

    def add_remote_file(self, filename, url, authcfg):
        "Add file from URL"

        self._check_filename(filename)
        if filename in self:
            raise QgistValueError(tr('"filename" is present in cache'))

        raw_data = request_data(url, authcfg) # does check url and authcfg

        subdirs = self._get_cache_subdirs(filename)
        subpath = os.path.join(self._path, *subdirs)
        self._ensure_path(subpath)

        filepath = os.path.abspath(os.path.join(subpath, filename))
        if os.path.exists(filepath):
            raise QgistValueError(tr('internal error - full path to future cache file already exists'))

        try:
            with open(filepath, 'wb') as f:
                f.write(raw_data)
        except Exception as e:
            raise QgistValueError(tr('failed to write cache file'), e)

        if not zipfile.is_zipfile(filepath):
            raise QgistValueError(tr('based on its content, file appears to be no ZIP-file'))

        self._files[filename] = filepath

    def extract(self, filename, path, password = None):
        "Extract file from local cache to path"

        self._check_filename(filename)
        if filename not in self:
            raise QgistValueError(tr('"filename" is not present in cache'))
        if not isinstance(path, str):
            raise QgistTypeError(tr('"path" must be str'))
        if len(path) == 0:
            raise QgistValueError(tr('"path" must not be empty'))
        if not isinstance(password, str) and password is not None:
            raise QgistTypeError(tr('"password" must either be a str or None'))

        self._ensure_path(path)

        try:
            with zipfile.ZipFile(self._files[filename], 'r') as f:
                f.extractall(path = path, pwd = password)
        except Exception as e:
            raise QgistValueError(tr('failed to extract ZIP-file'), e)

    def get_file_entries(self, filename):
        "Get iterator of entires in file in local cache"

        self._check_filename(filename)
        if filename not in self:
            raise QgistValueError(tr('"filename" is not present in cache'))

        try:
            with zipfile.ZipFile(self._files[filename], 'r') as f:
                namelist = f.namelist()
        except Exception as e:
            raise QgistValueError(tr('failed to open ZIP-file'), e)

        return (name for name in namelist)

    def get_file_entry(self, filename, entryname, password = None):
        "Read entry from file in local cache"

        self._check_filename(filename)
        if filename not in self:
            raise QgistValueError(tr('"filename" is not present in cache'))
        if not isinstance(entryname, str):
            raise QgistTypeError(tr('"entry" must be str'))
        if len(entryname) == 0:
            raise QgistValueError(tr('"entry" must not be empty'))
        if entryname not in self.get_file_entries(filename):
            raise QgistValueError(tr('"entryname" is not present in ZIP-file'))
        if not isinstance(password, str) and password is not None:
            raise QgistTypeError(tr('"password" must either be a str or None'))

        try:
            with zipfile.ZipFile(self._files[filename], 'r') as f:
                with f.open(entryname, mode = 'r', pwd = password) as fe:
                    data = fe.read()
        except Exception as e:
            raise QgistValueError(tr('failed to read ZIP-file'), e)

        return data # bytes

    def clear(self):
        "Clear local cache, i.e. remove all of its files"

        for path in self._files.values():
            if not os.path.exists(path):
                raise QgistValueError(tr('internal error - file in cache was already deleted'))
            if not os.path.isfile(path):
                raise QgistValueError(tr('internal error - file in cache is actually not a file'))
            try:
                os.unlink(path)
            except Exception as e:
                raise QgistValueError(tr('failed to remove cache file'), e)

        self._files.clear()
