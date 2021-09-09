"""
Copyright 2020 Lightbend Inc.
Licensed under the Apache License, Version 2.0.
"""
import os
import pathlib

from setuptools import find_packages, setup

# Load version in akkaserverless package.
from setuptools.command.build_py import build_py

exec(open("akkaserverless/version.py").read())

PROTOBUF_VERSION = "master"

version = __version__  # noqa
name = "akkaserverless"

print(f"package name: {name}, version: {version}", flush=True)

proto_lib_roots = ["akkaserverless"]
#proto_roots = ["akkaserverless"]


class FetchBuildProtosCommand(build_py):
    """fetch libs and install the protocol buffer generated sources."""

    def run(self):
        os.system(f"scripts/prepare.sh {PROTOBUF_VERSION}")
        
        for proto_root in proto_lib_roots:
            for root, subdirs, files in os.walk(proto_root):
                for file in [f for f in files if f.endswith(".proto")]:
                    file_path = pathlib.Path(root) / file
                    destination = "."
                    print(f"compiling {file_path} to {destination}")
                    command = f"python -m grpc_tools.protoc {' '.join([' -I ' + i for i in proto_lib_roots])} --python_out={proto_root} --grpc_python_out={proto_root} {file_path}"  # noqa
                    os.system(command)
                    
                    # the hacking to get files matched up
                    file_wo_ext = str(file_path).replace(".proto", "")
                    command = f"perl -i -pe 's/from akkaserverless/from akkaserverless.akkaserverless/g' {file_wo_ext}_pb2.py"
                    os.system(command)
                    command = f"perl -i -pe 's/from akkaserverless/from akkaserverless.akkaserverless/g' {file_wo_ext}_pb2_grpc.py"
                    os.system(command)

        return super().run()


packages = find_packages(exclude=[])

print(f"packages: {packages}")
setup(
    name=name,
    version=version,
    url="https://github.com/jpollock/akkaserverless-python-sdk",
    license="Apache 2.0",
    description="Akka Serverless Python Support Library",
    packages=packages,
    package_data={
        "": ["*.proto"],
        "": []
    },
    #long_description=open("Description.md", "r").read(),
    #long_description_content_type="text/markdown",
    zip_safe=False,
    scripts=["bin/fetch-akkaserverless-pb.sh", "bin/compile.sh", "bin/prepare.sh", "bin/start.sh", "bin/docker_build.sh", "bin/docker_push.sh"],
    install_requires=[
        "attrs>=19.3.0",
        "google-api>=0.1.12",
        "googleapis-common-protos >= 1.51.0",
        "grpcio>=1.31.0",
        "grpcio-tools>=1.31.0",
        "protobuf>=3.11.3",
        "pytest>=6.2.4",
        "six>=1.14.0",
        "grpcio-reflection>=1.31.0",
        "docker",
    ],
    cmdclass={
        "build_py": FetchBuildProtosCommand,
    },
)

