**Utils monorepo: Peewee Utils**
==================================

Just some Python [Peewee ORM](https://github.com/coleifer/peewee) utils.


Usage
=====

---

See top docstring in [peewee_utils.py](peewee_utils/peewee_utils.py).

Local dir install
-----------------
To install this client in a Poetry project, from a local dir, add this to `pyproject.toml`:
```toml
[project]
...
dependencies = [
    "peewee-utils @ ../peewee-utils"
    # "peewee-utils @ file:///Users/myuser/workspace/utils-monorepo/peewee-utils"
]

[tool.poetry.dependencies]
# This section is required only when there are editable (develop = true) dependencies.
peewee-utils = {develop = true}
```

Github install
--------------
To install this client in a Poetry project, from Github, add this to `pyproject.toml`:
```toml
[project]
...
dependencies = [
    "peewee-utils @ git+https://github.com/puntonim/utils-monorepo#subdirectory=peewee-utils",
]
```

Pip install
-----------
```sh
$ pip install "peewee-utils @ git+https://github.com/puntonim/utils-monorepo#subdirectory=peewee-utils"
```


Development setup
=================

---

See [README.md](../README.md) in the root dir.
