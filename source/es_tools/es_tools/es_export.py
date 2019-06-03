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

import json

import boto3
import click
from elasticsearch import Elasticsearch, RequestsHttpConnection
from es_config import INDEX_NAME, FILE_NAME, TIMEOUT, ES_PORT
from pkg_resources import require
from requests_aws4auth import AWS4Auth


@click.command()
@click.option('-i', '--index', default=INDEX_NAME, metavar='<index>',
              help='Index name to export. Default: {name}'.format(name=INDEX_NAME))
@click.option('-f', '--file', default=FILE_NAME, metavar='<file>',
              help='JSON filename to export. Default: {name}'.format(name=FILE_NAME))
@click.option('-e', '--es-host', required=True, metavar='<host>', help='Elasticsearch host name or IP address.')
@click.option('-p', '--es-port', type=int, default=ES_PORT, metavar='<port>',
              help='Elasticsearch port number. Default is {port}'.format(port=ES_PORT))
@click.option('-t', '--timeout', type=int, default=TIMEOUT, metavar='<timeout>',
              help='Elasticsearch timeout connection. Default is {timeout}'.format(timeout=TIMEOUT))
@click.option(
    '-r', '--region', metavar='<region>', default='us-east-1',
    help='Change the region to run the program. Default is us-east-1')
@click.option('-vv', '--verbose', is_flag=True, default=False, help='Verbose output.')
@click.option('-v', '--version', is_flag=True, default=False, help='Display version number and exit.')
def cli_export(*args, **kwargs):
    """
    Elasticsearch Export program
    :return:
    """
    version = kwargs.pop('version')
    verbose = kwargs.pop('verbose')
    host = kwargs.pop('es_host')
    port = kwargs.pop('es_port')
    timeout = kwargs.pop('timeout')
    index = kwargs.pop('index')
    filename = kwargs.pop('file')

    # Import boto3 credentials
    session = boto3.Session()
    credentials = session.get_credentials()
    awsauth = None
    if credentials:
        region = kwargs.pop('region')
        awsauth = AWS4Auth(credentials.access_key, credentials.secret_key, region, 'es',
                           session_token=credentials.token)

    click.echo('Elasticsearch export utility version {0}'.format(require("es_tools")[0].version))
    if version:
        return

    es = Elasticsearch([{'host': host, 'port': port}], timeout=timeout, http_auth=awsauth,
                       connection_class=RequestsHttpConnection)
    output = open(filename, 'wb')
    mapping = es.indices.get_mapping(index)
    click.echo('[+] Extracting {name} mapping'.format(name=INDEX_NAME))
    if verbose:
        click.echo(json.dumps(mapping[index]))
    output.write(json.dumps(mapping[index]))
    output.write('\n')

    results = es.search(index=index, body={"query": {"match_all": {}}}, scroll='10m', size=10000)
    click.echo('[+] Extracting {name} Documents'.format(name=INDEX_NAME))
    documents = results['hits']['hits']
    for doc in documents:
        doc.pop('_index', None)
        doc.pop('_score', None)
        if verbose:
            click.echo(json.dumps(doc))
        output.write(json.dumps(doc))
        output.write('\n')
    output.close()
    click.echo('[=] Finished processing')


if __name__ == "__main__":
    cli_export()
