**👴 Utils monorepo: Pydantic Utils**
=====================================

Just some Python Pydantic utils.


⚡ Usage
=======

---

See top docstrings in [pydantic_utils.py](pydantic_utils/pydantic_utils.py)
 and [pydantic_testutils.py](pydantic_utils/pydantic_testutils.py).

Poetry install
--------------
From Github:
```sh
$ poetry add git+https://github.com/puntonim/utils-monorepo#subdirectory=pydantic-utils
# at a specific version:
$ poetry add git+https://github.com/puntonim/utils-monorepo@3da9603977a5e2948429627ac83309353cca693d#subdirectory=pydantic-utils
```

From a local dir:
```sh
$ poetry add ../utils-monorepo/pydantic-utils/
$ poetry add "pydantic-utils @ file:///Users/myuser/workspace/utils-monorepo/pydantic-utils/"
```

Pip install
-----------
Same syntax as Poetry, but change `poetry add` with `pip install`.


🛠️ Development setup
====================

---

See [README.md](../README.md) in the root dir.


🚀 Deployment
=============

---

*Not deployed* as it can be (pip-)installed directly from Github o local dir 
 (see Usage section).\
And *not versioned* as when (pip-)installing from Github, it is possible to choose
 any version with a hash commit (see Usage section).


©️ Copyright
============

---

Copyright puntonim (https://github.com/puntonim). No License.
