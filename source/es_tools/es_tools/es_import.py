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
from es_config import INDEX_NAME, FILE_NAME
from pkg_resources import require
from requests_aws4auth import AWS4Auth


@click.command()
@click.option('-i', '--index', default=INDEX_NAME, metavar='<index>',
              help='Index name to export. Default: {name}'.format(name=INDEX_NAME))
@click.option('-f', '--file', required=True, metavar='<file>', default='export.json', type=click.File('rb'),
              help='JSON filename to import in the Elasticsearch. Default: {name}'.format(name=FILE_NAME))
@click.option('-e', '--es-host', required=True, metavar='<host>', help='Elasticsearch host name or IP address.')
@click.option('-p', '--es-port', type=int, default=80, metavar='<port>',
              help='Elasticsearch port number. Default is 80')
@click.option('-t', '--timeout', type=int, default=30, metavar='<timeout>',
              help='Elasticsearch timeout connection. Default is 30')
@click.option('-di', '--delete-index', is_flag=True, default=False,
              help='Delete current index before import. Default: false')
@click.option(
    '-r', '--region', metavar='<region>', default='us-east-1',
    help='Change the region to run the program. Default is us-east-1')
@click.option('-v', '--version', is_flag=True, default=False, help='Display version number and exit.')
def cli_import(*args, **kwargs):
    """
    Elasticsearch Import program
    :return:
    """
    version = kwargs.pop('version')
    host = kwargs.pop('es_host')
    port = kwargs.pop('es_port')
    timeout = kwargs.pop('timeout')
    index = kwargs.pop('index')
    delete_index = kwargs.pop('delete_index')
    filename = kwargs.pop('file')
    # Import boto3 credentials
    session = boto3.Session()
    credentials = session.get_credentials()
    awsauth = None
    if credentials:
        region = kwargs.pop('region')
        awsauth = AWS4Auth(credentials.access_key, credentials.secret_key, region, 'es',
                           session_token=credentials.token)

    click.echo('Elasticsearch import utility version {0}'.format(require("es_tools")[0].version))
    if version:
        return

    click.echo('[+] Connecting to ES: {host}:{port}'.format(host=host, port=port))
    es = Elasticsearch([{'host': host, 'port': port}], timeout=timeout, http_auth=awsauth,
                       connection_class=RequestsHttpConnection)

    documents = list(json.loads(doc) for doc in filename.readlines())

    if delete_index:
        click.echo('[-] Deleting current index: {}'.format(index))
        es.indices.delete(index, ignore=404)
    click.echo('[+] Creating {name} mapping'.format(name=INDEX_NAME))
    es.indices.create(index, body={'mappings': documents[0]['mappings']}, ignore=400)
    # Remove mappings from list
    documents.pop(0)

    click.echo('[+] Creating {name} Documents'.format(name=INDEX_NAME))
    for doc in documents:
        try:
            response = es.index(index=INDEX_NAME, doc_type=doc.pop('_type'), body=json.dumps(doc.pop('_source')),
                                id=doc.pop('_id'))
        except Exception as e:
            click.echo(e.error)

    click.echo('[=] Finished processing')


if __name__ == "__main__":
    cli_import()
