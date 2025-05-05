
**Utils monorepo: Text Utils**
==================================

Just some Python text utils.


Usage
=====

---

See top docstrings in [text_utils.py](text_utils/text_utils.py).

Local dir install
-----------------
To install this client in a Poetry project, from a local dir, add this to `pyproject.toml`:
```toml
[project]
...
dependencies = [
    "text-utils @ ../text-utils"
    # "text-utils @ file:///Users/myuser/workspace/utils-monorepo/text-utils"
]

[tool.poetry.dependencies]
# This section is required only when there are editable (develop = true) dependencies.
text-utils = {develop = true}
```

Github install
--------------
To install this client in a Poetry project, from Github, add this to `pyproject.toml`:
```toml
[project]
...
dependencies = [
    "text-utils @ git+https://github.com/puntonim/utils-monorepo#subdirectory=text-utils",
]
```

Pip install
-----------
```sh
$ pip install "text-utils @ git+https://github.com/puntonim/utils-monorepo#subdirectory=text-utils"
```


Development setup
=================

---

See [README.md](../README.md) in the root dir.
