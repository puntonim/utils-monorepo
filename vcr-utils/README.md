**📼 Utils monorepo: VCR Utils**
================================

Just some Python VCR utils to record stubs in tests.\
It's like [VCR.py](https://vcrpy.readthedocs.io/) but not limited to HTTP interactions.\
Instead, it stubs an entire function/method (via pickle) and replays it back later.


⚡ Usage
=======

---

See top docstrings in [vcr_utils.py](vcr_utils/vcr_utils.py).

Poetry install
--------------
From Github:
```sh
$ poetry add git+https://github.com/puntonim/utils-monorepo#subdirectory=vcr-utils
# at a specific version:
$ poetry add git+https://github.com/puntonim/utils-monorepo@3da9603977a5e2948429627ac83309353cca693d#subdirectory=vcr-utils
```

From a local dir:
```sh
$ poetry add ../utils-monorepo/vcr-utils/
$ poetry add "vcr-utils @ file:///Users/myuser/workspace/utils-monorepo/vcr-utils/"
```

Pip install
-----------
Same syntax as Poetry, but change `poetry add` with `pip install`.


🛠️ Development setup
====================

---

See [README.md](../README.md) in the root dir.


🚀 Deployment
=============

---

These utils are not deployed to PyPI.


©️ Copyright
============

---

Copyright puntonim (https://github.com/puntonim). No License.
