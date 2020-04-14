# -*- coding: utf-8 -*-

"""

QGIST PLUGIN MANAGER
QGIS Plugin for Managing QGIS Plugins
https://github.com/qgist/pluginmanager

    qgist/pluginmanager/dtype_import.py: Importing and tracking plugin modules

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

from .abc import imports_abc

from ..error import QgistTypeError
from ..util import tr

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

    def __init__(self, modules, module_names):

        if not isinstance(modules, dict):
            raise QgistTypeError(tr('"modules" must be a dict'))
        # TODO check modules content
        if not isinstance(module_names, dict):
            raise QgistTypeError(tr('"module_names" must be a dict'))
        # TODO check module_names content

        self._modules = modules
        self._module_names = module_names

    def __repr__(self):

        return f'<imports modules={len(self._modules):d} names={len(self._module_names):d}>'
