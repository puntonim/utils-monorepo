**Utils monorepo: Pydantic Utils**
==================================

Just some Python Pydantic utils.


Usage
=====

---

See top docstrings in [pydantic_utils.py](pydantic_utils/pydantic_utils.py)
 and [pydantic_testutils.py](pydantic_utils/pydantic_testutils.py).

Local dir install
-----------------
To install this client in a Poetry project, from a local dir, add this to `pyproject.toml`:
```toml
[project]
...
dependencies = [
    "pydantic-utils @ ../pydantic-utils"
    # "pydantic-utils @ file:///Users/myuser/workspace/utils-monorepo/pydantic-utils"
]

[tool.poetry.dependencies]
# This section is required only when there are editable (develop = true) dependencies.
pydantic-utils = {develop = true}
```

Github install
--------------
To install this client in a Poetry project, from Github, add this to `pyproject.toml`:
```toml
[project]
...
dependencies = [
    "pydantic-utils @ git+https://github.com/puntonim/utils-monorepo#subdirectory=pydantic-utils",
]
```

Pip install
-----------
```sh
$ pip install "pydantic-utils @ git+https://github.com/puntonim/utils-monorepo#subdirectory=pydantic-utils"
```


Development setup
=================

---

See [README.md](../README.md) in the root dir.
