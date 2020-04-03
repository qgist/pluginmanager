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
# IMPORT (Internal)
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

from .dtype_settings import dtype_settings_class
from .dtype_metadata import dtype_metadata_class
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
        has_processingprovider, has_serverfuncs, experimental,
        meta
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
        if not isinstance(meta, dtype_metadata_class):
            raise QgistTypeError(tr('"meta" must be meta data.'))

        self._id = plugin_id
        self._version = version
        self._has_processingprovider = has_processingprovider
        self._has_serverfuncs = has_serverfuncs
        self._experimental = experimental
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

    @classmethod
    def from_metadata(cls, meta):

        if not isinstance(meta, dtype_metadata_class):
            raise QgistTypeError(tr('"meta" must be meta data.'))

        return cls(
            plugin_id = meta['id'],
            version = dtype_version_class.from_pluginversion(meta['version']),
            has_processingprovider = meta['hasProcessingProvider'],
            has_serverfuncs = meta['server'],
            experimental = meta['experimental'],
            meta = meta,
            )
