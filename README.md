# Akka Serverless Python SDK

Source code for the Akka Serverless Python package.

For more information see the documentation for [implementing Akka Serverless services in JavaScript](https://developer.lightbend.com/docs/akka-serverless/javascript/).


This package is a fork of the original [Python SDK](https://github.com/cloudstateio/python-support) for [Cloudstate](https://cloudstate.io/). This Akka Serverless package is heavily indebted to the [C]loudstate contributors](https://github.com/cloudstateio/python-support/graphs/contributors), especially [Adriano Santos](https://github.com/sleipnir) and [Marcel Lanz](https://github.com/marcellanz).

## Installation via source

```
> git clone https://github.com/jpollock/akkaserverless-python-sdk.git
Cloning into 'akkaserverless-python-sdk'...

> cd akkaserverless-python-sdk
> python3 -m venv ./venv 
> source ./venv/bin/activate
> python --version     
Python 3.7.3
> pip --version 
> pip install wheel
> pip install .
```

### generate installer
```
python setup.py bdist_wheel
```

### local install
```
python -m pip install dist/akkaserverless-<the version>-py3-none-any.whl
```

### build and run tck, including provisional tests for stateless functions. 

NOTE: TODO; this is not setup or developed.

```
./extended_tck.sh
```