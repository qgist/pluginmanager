# Relevant Conda commands / API calls

`conda list --json` lists installed packages. It produces:

```json
[
{
  "base_url": "https://repo.anaconda.com/pkgs/main",
  "build_number": 3,
  "build_string": "h7b6447c_3",
  "channel": "pkgs/main",
  "dist_name": "zlib-1.2.11-h7b6447c_3",
  "name": "zlib",
  "platform": "linux-64",
  "version": "1.2.11"
},
{
  "base_url": "https://conda.anaconda.org/conda-forge",
  "build_number": 1,
  "build_string": "h3b9ef0a_1",
  "channel": "conda-forge",
  "dist_name": "zstd-1.4.4-h3b9ef0a_1",
  "name": "zstd",
  "platform": "linux-64",
  "version": "1.4.4"
}
]
```

`conda search -c intel --json` lists packages available from a channel. It produces:

```json
{
  "zstd": [
    {
      "arch": null,
      "build": "h84994c4_0",
      "build_number": 0,
      "channel": "https://repo.anaconda.com/pkgs/main/linux-64",
      "constrains": [],
      "depends": [
        "libgcc-ng >=7.2.0",
        "zlib >=1.2.11,<1.3.0a0"
      ],
      "fn": "zstd-1.3.3-h84994c4_0.conda",
      "legacy_bz2_md5": "8fd394fad0526da0465637434e03263f",
      "legacy_bz2_size": 860489,
      "license": "BSD 3-Clause",
      "md5": "73fea7c8a2218e7e446ee5f908e1e40d",
      "name": "zstd",
      "platform": null,
      "sha256": "9c31f2544006a792d2713cf04a0b4f734c34a86ed6ddcf8a94e6ebe8e2a42c24",
      "size": 627651,
      "subdir": "linux-64",
      "timestamp": 1529361748345,
      "url": "https://repo.anaconda.com/pkgs/main/linux-64/zstd-1.3.3-h84994c4_0.conda",
      "version": "1.3.3"
    },
    {
      "arch": null,
      "build": "h0b5b093_0",
      "build_number": 0,
      "channel": "https://repo.anaconda.com/pkgs/main/linux-64",
      "constrains": [],
      "depends": [
        "libgcc-ng >=7.3.0",
        "libstdcxx-ng >=7.3.0",
        "xz >=5.2.4,<6.0a0",
        "zlib >=1.2.11,<1.3.0a0"
      ],
      "fn": "zstd-1.3.7-h0b5b093_0.conda",
      "legacy_bz2_md5": "79121f98f7c307c15e95e8cba48280d2",
      "legacy_bz2_size": 908297,
      "license": "BSD 3-Clause",
      "license_family": "BSD",
      "md5": "9789e38cd4216c52f7d740625c49de79",
      "name": "zstd",
      "platform": null,
      "sha256": "8b676d98d30542a7ee550ee3b5f0cab6d5eb012d125dcc4b985eaf66d95d1e90",
      "size": 410326,
      "subdir": "linux-64",
      "timestamp": 1541459808645,
      "url": "https://repo.anaconda.com/pkgs/main/linux-64/zstd-1.3.7-h0b5b093_0.conda",
      "version": "1.3.7"
    },
    {
      "arch": "x86_64",
      "build": "hf484d3e_1",
      "build_number": 1,
      "channel": "https://conda.anaconda.org/intel/linux-64",
      "constrains": [],
      "depends": [
        "intelpython >=2019.0",
        "libgcc-ng >=7.3.0",
        "libstdcxx-ng >=7.3.0",
        "lz4-c >=1.8.1.2,<1.9.0a0",
        "xz >=5.2.4,<6.0a0",
        "zlib >=1.2.11,<1.3.0a0"
      ],
      "fn": "zstd-1.4.0-hf484d3e_1.tar.bz2",
      "license": "BSD 3-Clause",
      "license_family": "BSD",
      "md5": "9edb6780a9e90d54804b525e42655c0f",
      "name": "zstd",
      "platform": "linux",
      "size": 976565,
      "subdir": "linux-64",
      "timestamp": 1574454752203,
      "url": "https://conda.anaconda.org/intel/linux-64/zstd-1.4.0-hf484d3e_1.tar.bz2",
      "version": "1.4.0"
    }
  ]
}
```

`conda install -d --json --yes -c conda-forge pandas` installs a package (remove `-d`). It produces:

```json
{
  "actions": {
    "FETCH": [
      {
        "arch": null,
        "build": "h516909a_0",
        "build_number": 0,
        "channel": "https://conda.anaconda.org/conda-forge/linux-64",
        "constrains": [],
        "depends": [
          "ca-certificates",
          "libgcc-ng >=7.3.0"
        ],
        "fn": "openssl-1.1.1e-h516909a_0.tar.bz2",
        "license": "OpenSSL",
        "license_family": "Apache",
        "md5": "16cf7bab1f999de3c70f9770abc92587",
        "name": "openssl",
        "platform": null,
        "sha256": "3c5aabbcdff7669e460e6e4fc80d73ff0b7e595bff0cb1ea950973cd1b3979a1",
        "size": 2240683,
        "subdir": "linux-64",
        "timestamp": 1584558499807,
        "url": "https://conda.anaconda.org/conda-forge/linux-64/openssl-1.1.1e-h516909a_0.tar.bz2",
        "version": "1.1.1e"
      },
      {
        "arch": null,
        "build": "py37hc8dfbb8_1",
        "build_number": 1,
        "channel": "https://conda.anaconda.org/conda-forge/linux-64",
        "constrains": [],
        "depends": [
          "python >=3.7,<3.8.0a0",
          "python_abi 3.7.* *_cp37m"
        ],
        "fn": "certifi-2019.11.28-py37hc8dfbb8_1.tar.bz2",
        "license": "ISC",
        "md5": "2b0af186c6cd010f4c57f72106984e9a",
        "name": "certifi",
        "platform": null,
        "sha256": "4f3229c279b9ebb85ab0bab581d4746170cdcf5b00766463a5eb2121bcd63660",
        "size": 152198,
        "subdir": "linux-64",
        "timestamp": 1583921721896,
        "url": "https://conda.anaconda.org/conda-forge/linux-64/certifi-2019.11.28-py37hc8dfbb8_1.tar.bz2",
        "version": "2019.11.28"
      },
      {
        "arch": null,
        "build": "1_cp37m",
        "build_number": 1,
        "channel": "https://conda.anaconda.org/conda-forge/linux-64",
        "constrains": [
          "pypy <0a0",
          "python_abi * *_cp37m"
        ],
        "depends": [
          "python 3.7.*"
        ],
        "fn": "python_abi-3.7-1_cp37m.tar.bz2",
        "license": "BSD-3-Clause",
        "license_family": "BSD",
        "md5": "658a5c3d766bfc6574480204b10a6f20",
        "name": "python_abi",
        "platform": null,
        "sha256": "d530fd5472cfcb71ee4621c6792c4bc5c50ed09000f2cc1ac7a607f6ca8c50d9",
        "size": 3779,
        "subdir": "linux-64",
        "timestamp": 1583344659579,
        "url": "https://conda.anaconda.org/conda-forge/linux-64/python_abi-3.7-1_cp37m.tar.bz2",
        "version": "3.7"
      },
      {
        "arch": null,
        "build": "py37h0da4684_0",
        "build_number": 0,
        "channel": "https://conda.anaconda.org/conda-forge/linux-64",
        "constrains": [],
        "depends": [
          "libgcc-ng >=7.3.0",
          "libstdcxx-ng >=7.3.0",
          "numpy >=1.14.6,<2.0a0",
          "python >=3.7,<3.8.0a0",
          "python-dateutil >=2.6.1",
          "python_abi 3.7.* *_cp37m",
          "pytz >=2017.2"
        ],
        "fn": "pandas-1.0.3-py37h0da4684_0.tar.bz2",
        "license": "BSD 3-clause",
        "md5": "130ea975709db545d0c7e3ad34a5e9df",
        "name": "pandas",
        "platform": null,
        "sha256": "0fe688f6b24050b208105490cf6377b27a8aa87ece08b9b3929e804e4382c2ae",
        "size": 11644204,
        "subdir": "linux-64",
        "timestamp": 1584549253020,
        "url": "https://conda.anaconda.org/conda-forge/linux-64/pandas-1.0.3-py37h0da4684_0.tar.bz2",
        "version": "1.0.3"
      }
    ],
    "LINK": [
      {
        "base_url": "https://conda.anaconda.org/conda-forge",
        "build_number": 0,
        "build_string": "hecc5488_0",
        "channel": "conda-forge",
        "dist_name": "ca-certificates-2019.11.28-hecc5488_0",
        "name": "ca-certificates",
        "platform": "linux-64",
        "version": "2019.11.28"
      },
      {
        "base_url": "https://conda.anaconda.org/conda-forge",
        "build_number": 0,
        "build_string": "h516909a_0",
        "channel": "conda-forge",
        "dist_name": "openssl-1.1.1e-h516909a_0",
        "name": "openssl",
        "platform": "linux-64",
        "version": "1.1.1e"
      },
      {
        "base_url": "https://conda.anaconda.org/conda-forge",
        "build_number": 1,
        "build_string": "1_cp37m",
        "channel": "conda-forge",
        "dist_name": "python_abi-3.7-1_cp37m",
        "name": "python_abi",
        "platform": "linux-64",
        "version": "3.7"
      },
      {
        "base_url": "https://conda.anaconda.org/conda-forge",
        "build_number": 1,
        "build_string": "py37hc8dfbb8_1",
        "channel": "conda-forge",
        "dist_name": "certifi-2019.11.28-py37hc8dfbb8_1",
        "name": "certifi",
        "platform": "linux-64",
        "version": "2019.11.28"
      },
      {
        "base_url": "https://conda.anaconda.org/conda-forge",
        "build_number": 0,
        "build_string": "py37h0da4684_0",
        "channel": "conda-forge",
        "dist_name": "pandas-1.0.3-py37h0da4684_0",
        "name": "pandas",
        "platform": "linux-64",
        "version": "1.0.3"
      }
    ],
    "PREFIX": "/home/ernst/Desktop/SOFTWARE/conda/3/envs/qgis_py37",
    "UNLINK": [
      {
        "base_url": "https://repo.anaconda.com/pkgs/main",
        "build_number": 0,
        "build_string": "py37_0",
        "channel": "pkgs/main",
        "dist_name": "certifi-2019.11.28-py37_0",
        "name": "certifi",
        "platform": "linux-64",
        "version": "2019.11.28"
      },
      {
        "base_url": "https://repo.anaconda.com/pkgs/main",
        "build_number": 4,
        "build_string": "h7b6447c_4",
        "channel": "pkgs/main",
        "dist_name": "openssl-1.1.1d-h7b6447c_4",
        "name": "openssl",
        "platform": "linux-64",
        "version": "1.1.1d"
      },
      {
        "base_url": "https://repo.anaconda.com/pkgs/main",
        "build_number": 0,
        "build_string": "0",
        "channel": "pkgs/main",
        "dist_name": "ca-certificates-2020.1.1-0",
        "name": "ca-certificates",
        "platform": "linux-64",
        "version": "2020.1.1"
      }
    ]
  },
  "dry_run": true,
  "prefix": "$CONDA/envs/$ENV",
  "success": true
}
```

`conda uninstall -d --json --yes jupyterlab` uninstalls correspondingly (without `-d`).

An error uninstalling `pandas` (which is not present):

```json
{
  "caused_by": "None",
  "channel_urls": [],
  "channels_formatted": [],
  "error": "PackagesNotFoundError: The following packages are missing from the target environment:\n  - pandas\n",
  "exception_name": "PackagesNotFoundError",
  "exception_type": "<class 'conda.exceptions.PackagesNotFoundError'>",
  "message": "The following packages are missing from the target environment:\n  - pandas\n",
  "packages": [
    "pandas"
  ],
  "packages_formatted": "  - pandas"
}
```

An error installing `foobarfooo`, which does not exist:

```json
{
  "caused_by": "None",
  "channel_urls": [
    "https://conda.anaconda.org/conda-forge/linux-64",
    "https://conda.anaconda.org/conda-forge/noarch",
    "https://repo.anaconda.com/pkgs/main/linux-64",
    "https://repo.anaconda.com/pkgs/main/noarch",
    "https://repo.anaconda.com/pkgs/r/linux-64",
    "https://repo.anaconda.com/pkgs/r/noarch"
  ],
  "channels_formatted": "  - https://conda.anaconda.org/conda-forge/linux-64\n  - https://conda.anaconda.org/conda-forge/noarch\n  - https://repo.anaconda.com/pkgs/main/linux-64\n  - https://repo.anaconda.com/pkgs/main/noarch\n  - https://repo.anaconda.com/pkgs/r/linux-64\n  - https://repo.anaconda.com/pkgs/r/noarch",
  "error": "PackagesNotFoundError: The following packages are not available from current channels:\n\n  - foobarfooo\n\nCurrent channels:\n\n  - https://conda.anaconda.org/conda-forge/linux-64\n  - https://conda.anaconda.org/conda-forge/noarch\n  - https://repo.anaconda.com/pkgs/main/linux-64\n  - https://repo.anaconda.com/pkgs/main/noarch\n  - https://repo.anaconda.com/pkgs/r/linux-64\n  - https://repo.anaconda.com/pkgs/r/noarch\n\nTo search for alternate channels that may provide the conda package you're\nlooking for, navigate to\n\n    https://anaconda.org\n\nand use the search bar at the top of the page.\n",
  "exception_name": "PackagesNotFoundError",
  "exception_type": "<class 'conda.exceptions.PackagesNotFoundError'>",
  "message": "The following packages are not available from current channels:\n\n  - foobarfooo\n\nCurrent channels:\n\n  - https://conda.anaconda.org/conda-forge/linux-64\n  - https://conda.anaconda.org/conda-forge/noarch\n  - https://repo.anaconda.com/pkgs/main/linux-64\n  - https://repo.anaconda.com/pkgs/main/noarch\n  - https://repo.anaconda.com/pkgs/r/linux-64\n  - https://repo.anaconda.com/pkgs/r/noarch\n\nTo search for alternate channels that may provide the conda package you're\nlooking for, navigate to\n\n    https://anaconda.org\n\nand use the search bar at the top of the page.\n",
  "packages": [
    "foobarfooo"
  ],
  "packages_formatted": "  - foobarfooo"
}
```
