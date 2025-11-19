**🪵 Utils monorepo: Log Utils**
================================

Just some Python logging utils.


⚡ Usage
=======
See top docstring in [log_adapter.py](log_utils/log_adapter.py).


Note: this lib comes with 3 extras:
 - `rich-adapter`: required by `RichAdapter`;
 - `loguru-adapter`: required by `LoguruAdapter`;
 - `powertools-adapter`: required by `PowertoolsLoggerAdapter`.

Poetry install
--------------
From Github:
```sh
$ poetry add git+https://github.com/puntonim/utils-monorepo#subdirectory=log-utils
# at a specific version:
$ poetry add git+https://github.com/puntonim/utils-monorepo@3da9603977a5e2948429627ac83309353cca693d#subdirectory=log-utils
# with the extra `rich-adapter`:
$ poetry add "git+https://github.com/puntonim/utils-monorepo#subdirectory=log-utils[rich-adapter]"
```

From a local dir:
```sh
$ poetry add ../utils-monorepo/log-utils/
$ poetry add "log-utils @ file:///Users/myuser/workspace/utils-monorepo/log-utils/"
# with the extra `rich-adapter`:
$ poetry add "../utils-monorepo/log-utils/[rich-adapter]"
```

Pip install
-----------
Same syntax as Poetry, but change `poetry add` with `pip install`.


🛠️ Development setup
====================
See [README.md](../README.md) in the root dir.


🚀 Deployment
=============
*Not deployed* as it can be (pip-)installed directly from Github o local dir 
 (see Usage section).\
And *not versioned* as when (pip-)installing from Github, it is possible to choose
 any version with a hash commit (see Usage section).


©️ Copyright
============
Copyright puntonim (https://github.com/puntonim). No License.
