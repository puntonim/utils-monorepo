**🐁 Utils monorepo: Peewee Utils**
===================================

Just some Python [Peewee ORM](https://github.com/coleifer/peewee) utils.


⚡ Usage
=======

---

See top docstring in [peewee_utils.py](peewee_utils/peewee_utils.py).

Poetry install
--------------
From Github:
```sh
$ poetry add git+https://github.com/puntonim/utils-monorepo#subdirectory=peewee-utils
# at a specific version:
$ poetry add git+https://github.com/puntonim/utils-monorepo@3da9603977a5e2948429627ac83309353cca693d#subdirectory=peewee-utils
```

From a local dir:
```sh
$ poetry add ../utils-monorepo/peewee-utils/
$ poetry add "peewee-utils @ file:///Users/myuser/workspace/utils-monorepo/peewee-utils/"
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
