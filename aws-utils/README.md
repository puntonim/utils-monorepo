**🟠 Utils monorepo: AWS Utils**
=================================

Just some Python AWS utils.

*Note: there are AWS clients in [clients-monorepo](https://github.com/puntonim/clients-monorepo) 
 like [aws-parameter-store-client](https://github.com/puntonim/clients-monorepo/tree/main/aws-parameter-store-client),
 however this code is here in `utils-monorepo` as it is just a set of minor utils.*


⚡ Usage
=======
See top docstrings in [aws_lambda_utils.py](aws_utils/aws_lambda_utils.py),
 [api_gateway_event_factory](aws_utils/aws_testfactories/api_gateway_event_factory.py)
 and all the other files.

Note: in order to use the util `aws_lambda_utils.redact_http_headers(...)` you need to 
 install the extra `lambda-redact-http-headers`.


Poetry install
--------------
From Github:
```sh
$ poetry add git+https://github.com/puntonim/utils-monorepo#subdirectory=aws-utils
# at a specific version:
$ poetry add git+https://github.com/puntonim/utils-monorepo@3da9603977a5e2948429627ac83309353cca693d#subdirectory=aws-utils
# with the extra `lambda-redact-http-headers`:
$ poetry add "git+https://github.com/puntonim/utils-monorepo#subdirectory=aws-utils[lambda-redact-http-headers]"
```

From a local dir:
```sh
$ poetry add ../utils-monorepo/aws-utils/
$ poetry add "aws-utils @ file:///Users/myuser/workspace/utils-monorepo/aws-utils/"
# with the extra `lambda-redact-http-headers`:
$ poetry add "../utils-monorepo/aws-utils/[lambda-redact-http-headers]"
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
