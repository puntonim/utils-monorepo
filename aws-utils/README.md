**Utils monorepo: AWS Utils**
==================================

Just some Python AWS utils.

*Note: there are AWS clients in [clients-monorepo](https://github.com/puntonim/clients-monorepo) 
 like [aws-parameter-store-client](https://github.com/puntonim/clients-monorepo/tree/main/aws-parameter-store-client),
 however this code is here in `utils-monorepo` as it is just a set of minor utils.*

Usage
=====

---

See top docstrings in [aws_lambda_utils.py](aws_utils/aws_lambda_utils.py),
 [api_gateway_event_factory](aws_utils/aws_testfactories/api_gateway_event_factory.py)
 and all the other files.


TODO
mention the extra aws-utils[lambda-redact-http-headers]
for redact_http_headers()





Local dir install
-----------------
To install this client in a Poetry project, from a local dir, add this to `pyproject.toml`:
```toml
[project]
...
dependencies = [
    "aws-utils @ ../aws-utils"
    # "aws-utils @ file:///Users/myuser/workspace/utils-monorepo/aws-utils"
]

[tool.poetry.dependencies]
# This section is required only when there are editable (develop = true) dependencies.
aws-utils = {develop = true}
```
or:
```sh
$ poetry add ../aws-utils
```

Github install
--------------
To install this client in a Poetry project, from Github, add this to `pyproject.toml`:
```toml
[project]
...
dependencies = [
    "aws-utils @ git+https://github.com/puntonim/utils-monorepo#subdirectory=aws-utils",
]
```
or:
```sh
$ poetry add git+https://github.com/puntonim/utils-monorepo#subdirectory=aws-utils
```

Pip install
-----------
```sh
$ pip install "aws-utils @ git+https://github.com/puntonim/utils-monorepo#subdirectory=aws-utils"
```


Development setup
=================

---

See [README.md](../README.md) in the root dir.
