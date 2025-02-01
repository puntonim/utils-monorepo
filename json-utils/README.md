**Utils monorepo: JSON Utils**
==================================

Just some Python JSON utils.


Usage
=====

See top docstrings in [json_utils.py](json_utils/json_utils.py).

---

Local dir install
-----------------
To install this client in a Poetry project, from a local dir, add this to `pyproject.toml`:
```toml
[project]
...
dependencies = [
    "json-utils @ ../json-utils"
    # "json-utils @ file:///Users/myuser/workspace/utils-monorepo/json-utils"
]

[tool.poetry.dependencies]
# This section is required only when there are editable (develop = true) dependencies.
json-utils = {develop = true}
```

Github install
--------------
To install this client in a Poetry project, from Github, add this to `pyproject.toml`:
```toml
[project]
...
dependencies = [
    "json-utils @ git+https://github.com/puntonim/utils-monorepo#subdirectory=json-utils",
]
```

Pip install
-----------
```sh
$ pip install "json-utils @ git+https://github.com/puntonim/utils-monorepo#subdirectory=json-utils"
```


Development setup
=================

---

See [README.md](../README.md) in the root dir.
