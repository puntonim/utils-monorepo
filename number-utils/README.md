**Utils monorepo: Number Utils**
================================

Just some Python number utils.


Usage
=====

---

See top docstrings in [number_utils.py](number_utils/number_utils.py).

Local dir install
-----------------
To install this client in a Poetry project, from a local dir, add this to `pyproject.toml`:
```toml
[project]
...
dependencies = [
    "number-utils @ ../number-utils"
    # "number-utils @ file:///Users/myuser/workspace/utils-monorepo/number-utils"
]

[tool.poetry.dependencies]
# This section is required only when there are editable (develop = true) dependencies.
number-utils = {develop = true}
```

Github install
--------------
To install this client in a Poetry project, from Github, add this to `pyproject.toml`:
```toml
[project]
...
dependencies = [
    "number-utils @ git+https://github.com/puntonim/utils-monorepo#subdirectory=number-utils",
]
```

Pip install
-----------
```sh
$ pip install "number-utils @ git+https://github.com/puntonim/utils-monorepo#subdirectory=number-utils"
```


Development setup
=================

---

See [README.md](../README.md) in the root dir.
