**⚙️ Utils monorepo: Settings Utils**
=====================================

Just some Python settings utils.


⚡ Usage
=======

---

See top docstrings in [settings_utils.py](settings_utils/settings_utils.py)
 and [settings_testutils.py](settings_utils/settings_testutils.py).

Note: in order to use the util `settings_utils.get_string_from_env_or_aws_parameter_store(...)` you 
 need to install the extra `get-from-aws-param-store`.


Poetry install
--------------
From Github:
```sh
$ poetry add git+https://github.com/puntonim/utils-monorepo#subdirectory=settings-utils
# at a specific version:
$ poetry add git+https://github.com/puntonim/utils-monorepo@3da9603977a5e2948429627ac83309353cca693d#subdirectory=settings-utils
# with the extra `get-from-aws-param-store`:
$ poetry add "git+https://github.com/puntonim/utils-monorepo#subdirectory=settings-utils[get-from-aws-param-store]"
```

From a local dir:
```sh
$ poetry add ../utils-monorepo/settings-utils/
$ poetry add "settings-utils @ file:///Users/myuser/workspace/utils-monorepo/settings-utils/"
# with the extra `get-from-aws-param-store`:
$ poetry add "../utils-monorepo/settings-utils/[get-from-aws-param-store]"
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

*Not deployed* as it can be (pip-)installed directly from Github o local dir 
 (see Usage section).\
And *not versioned* as when (pip-)installing from Github, it is possible to choose
 any version with a hash commit (see Usage section).


©️ Copyright
============

---

Copyright puntonim (https://github.com/puntonim). No License.
