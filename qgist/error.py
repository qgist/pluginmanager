# -*- coding: utf-8 -*-

"""

QGIST PLUGIN MANAGER
QGIS Plugin for Managing QGIS Plugins
https://github.com/qgist/pluginmanager

    qgist/error.py: QGIST errors

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
# EXCEPTIONS
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

class QgistAttributeError(AttributeError):
    pass

class QgistConfigFormatError(KeyError):
    pass

class QgistConfigKeyError(KeyError):
    pass

class QgistIndexError(IndexError):
    pass

class QgistRequestError(Exception):
    pass

class QgistTranslationError(Exception):
    pass

class QgistTypeError(TypeError):
    pass

class QgistValueError(ValueError):
    pass

class QgistNotImplementedError(NotImplementedError):
    pass

class QgistSyntaxError(SyntaxError):
    pass

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# ALL EXCEPTIONS
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

Qgist_ALL_Errors = tuple([v for k, v in globals().items() if k.startswith('Qgist')])
