**🛠️ Utils monorepo**
=====================

Just a collection of Python utils.

Each util is a standalone Python project that can be installed individually 
 from the subdir.


🎯 Target Python version
========================

---

The target is a Python version that is recent enough, but not too recent for a wide
 compatibility.\
Python 3.10 seems a good compromise.\

*Note: Python 3.10 introduced the annotation `| None` for optional types, among other things.*


🛠️ Development setup
====================

---

1 - System requirements
----------------------

**Python 3.10**\
The target Python 3.10 for a wide compatibility.\
Install it with pyenv:
```sh
$ pyenv install -l  # List all available versions.
$ pyenv install 3.10.16
```

**Poetry**\
Pipenv is used to manage requirements (and virtual environments).\
Read more about Poetry [here](https://python-poetry.org/). \
Follow the [install instructions](https://python-poetry.org/docs/#osx--linux--bashonwindows-install-instructions).

**Pre-commit**\
Pre-commit is used to format the code with black before each git commit:
```sh
$ pip install --user pre-commit
# On macOS you can also:
$ brew install pre-commit
```

2 - Virtual environment and requirements
----------------------------------------

Create a virtual environment and install all deps with one Make command:
```sh
$ make poetry-create-env
# Or to recreate:
$ make poetry-destroy-and-recreate-env
# Then you can activate the virtual env with:
$ eval $(poetry env activate)
# And later deactivate the virtual env with:
$ deactivate
```

Without using Makefile the full process is:
```sh
# Activate the Python version for the current project:
$ pyenv local 3.10  # It creates `.python-version`, to be git-ignored.
$ pyenv which python
/Users/nimiq/.pyenv/versions/3.10.16/bin/python

# Now create a venv with poetry:
$ poetry env use ~/.pyenv/versions/3.10.16/bin/python
# Now you can open a shell and/or install:
$ eval $(poetry env activate)
# And finally, install all requirements:
$ poetry install
# And later deactivate the virtual env with:
$ deactivate
```

To add new requirements:
```sh
$ poetry add requests

# Dev or test only.
$ poetry add -G test pytest
$ poetry add -G dev ipdb

# With extra reqs:
$ poetry add -G dev "aws-lambda-powertools[aws-sdk]"
$ poetry add "requests[security,socks]"

# From Git:
$ poetry add git+https://github.com/aladagemre/django-notification

# From a Git subdir:
$ poetry add git+https://github.com/puntonim/utils-monorepo#subdirectory=log-utils
# and with extra reqs:
$ poetry add "git+https://github.com/puntonim/utils-monorepo#subdirectory=log-utils[rich-adapter,loguru-adapter]"
# and at a specific version:
$ poetry add git+https://github.com/puntonim/utils-monorepo@00a49cb64524df19bf55ab5c7c1aaf4c09e92360#subdirectory=log-utils
# and at a specific version, with extra reqs:
$ poetry add "git+https://github.com/puntonim/utils-monorepo@00a49cb64524df19bf55ab5c7c1aaf4c09e92360#subdirectory=log-utils[rich-adapter,loguru-adapter]"

# From a local dir:
$ poetry add ../utils-monorepo/log-utils/
$ poetry add "log-utils @ file:///Users/myuser/workspace/utils-monorepo/log-utils/"
# and with extra reqs:
$ poetry add "../utils-monorepo/log-utils/[rich-adapter,loguru-adapter]"
# and I was able to choose a Git version only with pip (not poetry):
$ pip install "git+file:///Users/myuser/workspace/utils-monorepo@00a49cb64524df19bf55ab5c7c1aaf4c09e92360#subdirectory=log-utils" 
```

3 - Pre-commit
--------------

```sh
$ pre-commit install
```


🚀 Deployment
=============

---

These utils are not deployed to PyPI.\
See the individual `README.md` file in each util subdir to know how to install and use
 each util.


©️ Copyright
============

---

Copyright puntonim (https://github.com/puntonim). No License.
