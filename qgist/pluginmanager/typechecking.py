# -*- coding: utf-8 -*-

"""

QGIST PLUGIN MANAGER
QGIS Plugin for Managing QGIS Plugins
https://github.com/qgist/pluginmanager

    qgist/pluginmanager/typechecking.py: (Duck) typ checks

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

from ..error import (
    QgistTypeError,
    )

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# ROUTINES
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

def conforms_to_spec(obj, spec):
    "Checks whether object conforms with specification - returns bool"

    check_name = lambda o, n: n == getattr(o, '__name__', None)

    if not isinstance(spec, dict):
        raise QgistTypeError('spec must be a dict')
    if not all((isinstance(item, str) for item in spec.keys())):
        raise QgistTypeError('keys in spec dict must be str')

    name = spec.get('name', None)
    typename = spec.get('typename', None)
    attrs = spec.get('attrs', list())

    if not isinstance(name, str) and name is not None:
        raise QgistTypeError('name in spec must either be str or None or not specified')
    if not isinstance(typename, str) and typename is not None:
        raise QgistTypeError('typename in spec must either be str or None or not specified')
    if not isinstance(attrs, list):
        raise QgistTypeError('attrs in spec dict must be a list')
    if not all((isinstance(item, str) for item in attrs)):
        raise QgistTypeError('items in attrs in spec dict must be str')

    if not check_name(obj, name):
        return False
    if not check_name(type(obj), typename):
        return False
    if not all((hasattr(obj, attr) for attr in attrs)):
        return False

    return True
