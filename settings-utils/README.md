**Utils monorepo: Settings Utils**
==================================

Just some Python settings utils.


Usage
=====

---

See top docstrings in [settings_utils.py](settings_utils/settings_utils.py)
 and [settings_testutils.py](settings_utils/settings_testutils.py).

Local dir install
-----------------
To install this client in a Poetry project, from a local dir, add this to `pyproject.toml`:
```toml
[project]
...
dependencies = [
    "settings-utils @ ../settings-utils"
    # "settings-utils @ file:///Users/myuser/workspace/utils-monorepo/settings-utils"
]

[tool.poetry.dependencies]
# This section is required only when there are editable (develop = true) dependencies.
settings-utils = {develop = true}
```

Github install
--------------
To install this client in a Poetry project, from Github, add this to `pyproject.toml`:
```toml
[project]
...
dependencies = [
    "settings-utils @ git+https://github.com/puntonim/utils-monorepo#subdirectory=settings-utils",
]
```

Pip install
-----------
```sh
$ pip install "settings-utils @ git+https://github.com/puntonim/utils-monorepo#subdirectory=settings-utils"
```


Development setup
=================

---

See [README.md](../README.md) in the root dir.
