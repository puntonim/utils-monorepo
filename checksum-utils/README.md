**Utils monorepo: Checksum Utils**
==================================

Just some Python checksum utils.


Usage
=====

---

Local dir install
-----------------
To install this client in a Poetry project, from a local dir, add this to `pyproject.toml`:
```toml
[project]
...
dependencies = [
    "checksum-utils @ ../checksum-utils"
    # "checksum-utils @ file:///Users/myuser/workspace/utils-monorepo/checksum-utils"
]

[tool.poetry.dependencies]
# This section is required only when there are editable (develop = true) dependencies.
checksum-utils = {develop = true}
```

Github install
--------------
To install this client in a Poetry project, from Github, add this to `pyproject.toml`:
```toml
[project]
...
dependencies = [
    "checksum-utils @ git+https://github.com/puntonim/utils-monorepo#subdirectory=checksum-utils",
]
```

Pip install
-----------
```sh
$ pip install "checksum-utils @ git+https://github.com/puntonim/utils-monorepo#subdirectory=checksum-utils"
```


Development setup
=================

---

See [README.md](../README.md) in the root dir.
