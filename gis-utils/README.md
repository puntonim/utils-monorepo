**🌍 Utils monorepo: GIS Utils**
================================

Just some Python GIS (Geographic information system) utils.


⚡ Usage
=======
See top docstrings in [gis_utils.py](gis_utils/gis_utils.py).

Poetry install
--------------
From Github:
```sh
$ poetry add git+https://github.com/puntonim/utils-monorepo#subdirectory=gis-utils
# at a specific version:
$ poetry add git+https://github.com/puntonim/utils-monorepo@3da9603977a5e2948429627ac83309353cca693d#subdirectory=gis-utils
```

From a local dir:
```sh
$ poetry add ../utils-monorepo/gis-utils/
$ poetry add "gis-utils @ file:///Users/myuser/workspace/utils-monorepo/gis-utils/"
```

Pip install
-----------
Same syntax as Poetry, but change `poetry add` with `pip install`.


🛠️ Development setup
====================
See [README.md](../README.md) in the root dir.


🚀 Deployment
=============
*Not deployed* as it can be (pip-)installed directly from Github o local dir 
 (see Usage section).\
And *not versioned* as when (pip-)installing from Github, it is possible to choose
 any version with a hash commit (see Usage section).


©️ Copyright
============
Copyright puntonim (https://github.com/puntonim). No License.
