**Utils monorepo: VCR Utils**
==================================

Just some Python VCR utils to record stubs in tests.\
It's like [VCR.py](https://vcrpy.readthedocs.io/) but not limited to HTTP interactions.\
Instead, it stubs an entire function/method (via pickle) and replays it back later.


Usage
=====

---

See top docstrings in [vcr_utils.py](vcr_utils/vcr_utils.py).

Local dir install
-----------------
To install this client in a Poetry project, from a local dir, add this to `pyproject.toml`:
```toml
[project]
...
dependencies = [
    "vcr-utils @ ../vcr-utils"
    # "vcr-utils @ file:///Users/myuser/workspace/utils-monorepo/vcr-utils"
]

[tool.poetry.dependencies]
# This section is required only when there are editable (develop = true) dependencies.
vcr-utils = {develop = true}
```

Github install
--------------
To install this client in a Poetry project, from Github, add this to `pyproject.toml`:
```toml
[project]
...
dependencies = [
    "vcr-utils @ git+https://github.com/puntonim/utils-monorepo#subdirectory=vcr-utils",
]
```

Pip install
-----------
```sh
$ pip install "vcr-utils @ git+https://github.com/puntonim/utils-monorepo#subdirectory=vcr-utils"
```


Development setup
=================

---

See [README.md](../README.md) in the root dir.
