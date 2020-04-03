# -*- coding: utf-8 -*-

"""

QGIST PLUGIN MANAGER
QGIS Plugin for Managing QGIS Plugins
https://github.com/qgist/pluginmanager

    qgist/pluginmanager/backends/load.py: Detecting pluginmanager backends

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
import importlib
import os

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# IMPORT (Internal)
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

from ...error import QgistSyntaxError

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# CLASSES
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

class _inventory(dict):
    """
    Backend inventory (a dict, more or less)

    Mutable.
    """

    def __init__(self):
        super().__init__()
        path = os.path.dirname(__file__)
        backends = [
            (item[:-3], True) if item.lower().endswith('.py') else (item, False)
            for item in os.listdir(path) if not item.startswith('_')
            ]
        self.update({
            name: _backend(path, name, isfile) for name, isfile in backends
            })

        # for key in self.keys(): # TODO test!
        #     self[key].load_meta()
        #     self[key].load_module()

class _backend:
    """
    Backend descriptor with lazy loading of backend module, class and meta data

    Mutable.
    """

    def __init__(self, path, name, isfile):

        self._path = path
        self._name = name
        self._isfile = isfile
        self._module = None
        self._src = None
        self._meta = None

    def __getitem__(self, key):
        "provides access to backend meta data dict"

        if self._meta is None:
            raise QgistSyntaxError('backend metadata has not been loaded')
        return self._meta[key]

    @property
    def dtype_plugin_class(self):
        "returns backend plugin class"

        if self._module is None:
            raise QgistSyntaxError('backend module has not been loaded')
        return self._module.dtype_pluginrelease_class

    @property
    def dtype_repository_class(self):
        "returns backend repository class"

        if self._module is None:
            raise QgistSyntaxError('backend module has not been loaded')
        return self._module.dtype_repository_class

    def load_meta(self):
        "loads meta data from backend without importing it"

        with open(
            os.path.join(self._path, self._name + '.py')
            if self._isfile else
            os.path.join(self._path, self._name, '__init__.py'),
            'r'
            ) as f:
            self._src = f.read()
        self._meta = {k[2:-2]: v for k, v in _get_vars(self._src,
            *['__%s__' % item for item in (
                'longname',
                'description',
                )],
            ).items()}
        self._meta['name'] = self._name

    def load_module(self):
        "actually imports backend module"

        self._module = importlib.import_module('pluginmanager.qgist.pluginmanager.backends.%s' % self._name)

    def keys(self):
        "provides access to backend meta data dict keys"

        if self._meta is None:
            raise QgistSyntaxError('backend metadata has not been loaded')
        return self._meta.keys()

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# ROUTINES
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

def _get_vars(src, *names, default = None):
    "Gets variables from Python file without importing it"

    tree = ast.parse(src)
    out_dict = {name: default for name in names}
    for item in tree.body:
        if not isinstance(item, ast.Assign):
            continue
        for target in item.targets:
            if target.id not in names:
                continue
            out_dict[target.id] = _parse_tree(item.value)
    return out_dict

def _parse_tree(leaf):
    "Parses AST and returns Python data types (str, bytes, int, float, dict, list, tuple, set)"

    if isinstance(leaf, ast.Str) or isinstance(leaf, ast.Bytes):
        return leaf.s
    elif isinstance(leaf, ast.Num):
        return leaf.n
    elif isinstance(leaf, ast.NameConstant):
        return leaf.value
    elif isinstance(leaf, ast.Dict):
        return {
            _parse_tree(leaf_key): _parse_tree(leaf_value)
            for leaf_key, leaf_value in zip(leaf.keys, leaf.values)
            }
    elif isinstance(leaf, ast.List):
        return [_parse_tree(leaf_item) for leaf_item in leaf.elts]
    elif isinstance(leaf, ast.Tuple):
        return tuple([_parse_tree(leaf_item) for leaf_item in leaf.elts])
    elif isinstance(leaf, ast.Set):
        return {_parse_tree(leaf_item) for leaf_item in leaf.elts}
    else:
        raise QgistSyntaxError('unhandled data type: %s (%s)' % (str(leaf), str(dir(leaf))))

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# EXPORT
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

inventory = _inventory()
