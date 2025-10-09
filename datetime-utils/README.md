**Utils monorepo: Datetime Utils**
==================================

Just some Python date and time utils.


Usage
=====

---

See top docstrings in [datetime_utils.py](datetime_utils/datetime_utils.py)
 and [datetime_testutils.py](datetime_utils/datetime_testutils.py).

Local dir install
-----------------
To install this client in a Poetry project, from a local dir, add this to `pyproject.toml`:
```toml
[project]
...
dependencies = [
    "datetime-utils @ ../datetime-utils"
    # "datetime-utils @ file:///Users/myuser/workspace/utils-monorepo/datetime-utils"
]

[tool.poetry.dependencies]
# This section is required only when there are editable (develop = true) dependencies.
datetime-utils = {develop = true}
```
or:
```sh
$ poetry add ../datetime-utils
```

Github install
--------------
To install this client in a Poetry project, from Github, add this to `pyproject.toml`:
```toml
[project]
...
dependencies = [
    "datetime-utils @ git+https://github.com/puntonim/utils-monorepo#subdirectory=datetime-utils",
]
```
or:
```sh
$ poetry add git+https://github.com/puntonim/utils-monorepo#subdirectory=datetime-utils
```

Pip install
-----------
```sh
$ pip install "datetime-utils @ git+https://github.com/puntonim/utils-monorepo#subdirectory=datetime-utils"
```


Development setup
=================

---

See [README.md](../README.md) in the root dir.
