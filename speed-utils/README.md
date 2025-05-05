**Utils monorepo: Speed Utils**
===============================

Just some Python speed utils.


Usage
=====

---

See top docstrings in [speed_utils.py](speed_utils/speed_utils.py).

Local dir install
-----------------
To install this client in a Poetry project, from a local dir, add this to `pyproject.toml`:
```toml
[project]
...
dependencies = [
    "speed-utils @ ../speed-utils"
    # "speed-utils @ file:///Users/myuser/workspace/utils-monorepo/speed-utils"
]

[tool.poetry.dependencies]
# This section is required only when there are editable (develop = true) dependencies.
speed-utils = {develop = true}
```

Github install
--------------
To install this client in a Poetry project, from Github, add this to `pyproject.toml`:
```toml
[project]
...
dependencies = [
    "speed-utils @ git+https://github.com/puntonim/utils-monorepo#subdirectory=speed-utils",
]
```

Pip install
-----------
```sh
$ pip install "speed-utils @ git+https://github.com/puntonim/utils-monorepo#subdirectory=speed-utils"
```


Development setup
=================

---

See [README.md](../README.md) in the root dir.
