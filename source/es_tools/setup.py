#!/usr/bin/python
# -*- coding: utf-8 -*-
#####################################################################################################################
# Copyright 2019 Amazon.com, Inc. or its affiliates. All Rights Reserved.                                           #
#                                                                                                                   #
# Licensed under the Apache License, Version 2.0 (the "License"). You may not use this file except in compliance    #
# with the License. A copy of the License is located at                                                             #
#                                                                                                                   #
#     http://www.apache.org/licenses/LICENSE-2.0                                                                    #
#                                                                                                                   #
# or in the "license" file accompanying this file. This file is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES #
# OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing         #
# permissions and limitations under the License.                                                                    #
######################################################################################################################

import io
import os
import re
from setuptools import setup

def read(*names, **kwargs):
    with io.open(
        os.path.join(os.path.dirname(__file__), *names),
        encoding=kwargs.get("encoding", "utf8")
    ) as fp:
        return fp.read()


def find_version(*file_paths):
    version_file = read(*file_paths)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")

setup(
    name='es_tools',
    version=find_version("es_tools", "__init__.py"),
    packages=['es_tools'],
    url='',
    license='Apache 2.0',
    author='AWS Solutions Builders',
    description='Elasticsearch backup and restore for kibana dashboards',
    entry_points={
        'console_scripts': [
            'es-export = es_tools.es_export:cli_export',
            'es-import = es_tools.es_import:cli_import'
        ]

    },
    install_requires=[
        'boto3>=1.9.120',
        'click>=7.0',
        'elasticsearch>=6.0.0,<7.0.0',
        'requests_aws4auth>=0.9'
    ]
)
