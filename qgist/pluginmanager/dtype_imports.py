# -*- coding: utf-8 -*-

"""

QGIST PLUGIN MANAGER
QGIS Plugin for Managing QGIS Plugins
https://github.com/qgist/pluginmanager

    qgist/pluginmanager/dtype_imports.py: Importing and tracking plugin modules

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

import builtins
import os
import sys

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# IMPORT (Internal)
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

from .abc import (
    imports_abc,
    index_abc,
    )

from ..error import QgistTypeError
from ..util import tr
from ..qgis_api import get_builtin_import

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# CLASS: IMPORT
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

class dtype_imports_class(imports_abc):
    """
    Import module. Holds and manages Python modules (within interpreter)

    This should **REALLY* be atomic and handled by plugins themselves!
    This class only exists for compatibility with current `qgis.utils`.

    Mutable.
    """

    def __init__(self, modules, module_names, index):

        if not isinstance(modules, dict):
            raise QgistTypeError(tr('"modules" must be a dict'))
        # TODO check modules content
        if not isinstance(module_names, dict):
            raise QgistTypeError(tr('"module_names" must be a dict'))
        # TODO check module_names content
        if not isinstance(index, index_abc):
            raise QgistTypeError(tr('"index" must be an index'))

        self._modules = modules # holds return values of `package.classFactory(iface)` (from `_startPlugin`)
        self._module_names = module_names
        self._index = index

        self._builtin_import = get_builtin_import() # represents builtins.__import__

        self._import = None # call THIS from within this class
        self._old_import = None
        self._connect()

    def __repr__(self):

        return f'<imports modules={len(self._modules):d} names={len(self._module_names):d}>'

    def _wrapper_import(self, name, globals = None, locals = None, fromlist = (), level = 0):
        """
        Wrapper around builtin import that keeps track of loaded plugin modules
        and blocks certain unsafe imports.
        DO NOT CALL DIRECTLY! USE `dtype_imports_class._import` INSTEAD!
        """

        if 'PyQt4' in name:
            raise ImportError((
                'PyQt4 classes cannot be imported in QGIS 3.x. '
                f'Use {name.replace("PyQt4", "PyQt5"):s} or '
                f'the version independent {name.replace("PyQt4", "qgis.PyQt"):s} import instead.'
                ))

        mod = self._builtin_import(name, globals, locals, fromlist, level)

        if not mod and '__file__' not in mod.__dict__:
            return mod

        module_name = mod.__name__ if fromlist else name
        package_name = module_name.split('.')[0]

        # check whether the module belongs to one of our plugins
        if package_name not in self._index.plugins.keys(active = True):
            return mod

        if package_name not in self._module_names:
            self._module_names[package_name] = set()
        self._module_names[package_name].add(module_name)

        # check the fromlist for additional modules (from X import Y,Z)
        if fromlist: # not None, not empty
            for fromitem in fromlist:
                frmod = f'{module_name:s}.{fromitem:s}'
                if frmod in sys.modules:
                    self._module_names[package_name].add(frmod)

        return mod

    def _connect(self):
        "use our own implementation for builtins.__import__"

        if os.environ.get('QGIS_NO_OVERRIDE_IMPORT'):
            self._import = self._builtin_import
        else:
            def unbound_import_wrapper(*args, **kwargs):
                return self._wrapper_import(*args, **kwargs)
            self._import = unbound_import_wrapper

        self._old_import = builtins.__import__
        builtins.__import__ = self._import
