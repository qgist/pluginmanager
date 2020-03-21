# Data structures

Notes based on comment in `python/pyplugin_installer/installer_data.py`

## *mRepositories*: dict of dicts

```python
mRepositories = {
    repoName: {
        "url": unicode,
        "enabled": bool,
        "valid": bool,
        "Relay": Relay, # Relay object for transmitting signals from QPHttp with adding the repoName information
        "Request": QNetworkRequest,
        "xmlData": QNetworkReply,
        "state": int, # (0 - disabled, 1-loading, 2-loaded ok, 3-error (to be retried), 4-rejected)
        "error": unicode,
        }
    }
```

# *mPlugins*: dict of dicts

```python
mPlugins = {
    id: {
        "id": unicode,                     # module name
        "name": unicode,                   # human readable plugin name
        "description": unicode,            # short description of the plugin purpose only
        "about": unicode,                  # longer description: how does it work, where does it install, how to run it?
        "category": unicode,               # will be removed?
        "tags": unicode,                   # comma separated, spaces allowed
        "changelog": unicode,              # may be multiline
        "author_name": unicode,            # author name
        "author_email": unicode,           # author email
        "homepage": unicode,               # url to the plugin homepage
        "tracker": unicode,                # url to a tracker site
        "code_repository": unicode,        # url to the source code repository
        "version_installed": unicode,      # installed instance version
        "library": unicode,                # absolute path to the installed library / Python module
        "icon": unicode,                   # path to the first:(INSTALLED | AVAILABLE) icon
        "pythonic": const bool=True        # True if Python plugin
        "readonly": boolean,               # True if core plugin
        "installed": boolean,              # True if installed
        "available": boolean,              # True if available in repositories
        "status": unicode,                 # ( not installed | new ) | ( installed | upgradeable | orphan | newer )
        "error": unicode,                  # NULL | broken | incompatible | dependent
        "error_details": unicode,          # error description
        "experimental": boolean,           # true if experimental, false if stable
        "deprecated": boolean,             # true if deprecated, false if actual
        "trusted": boolean,                # true if trusted, false if not trusted
        "version_available": unicode,      # available version
        "zip_repository": unicode,         # the remote repository id
        "download_url": unicode,           # url for downloading the plugin
        "filename": unicode,               # the zip file name to be unzipped after downloaded
        "downloads": unicode,              # number of downloads
        "average_vote": unicode,           # average vote
        "rating_votes": unicode,           # number of votes
        "plugin_dependencies": unicode,    # PIP-style comma separated list of plugin dependencies
        }
    }
```

The **id** of a plugin equals the **name of its zip-file** (without its extension).

There is also `hasProcessingProvider` (either `yes` or `no`). See [commit](https://github.com/qgis/QGIS/commit/558d5365b574a4f9e96d32ecdd7220c57b148266).

## Translations

The following fields can be translated (i18n):

- name
- description
- about
- tags
