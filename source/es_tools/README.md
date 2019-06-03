Elastic Search tools
====================

This program is aimed to export and import kibana dashboards from/to Elastic Search clusters.
The default parameters are aimed to import/export the kibana dashboard that runs on AWS Elasticsearch Service with version 1.5 (The default kibana dashboard is .kibana-4)

You can run the tool to export/import virtually any index on Elasticsearch just pointing the index name. But the code has no performance optimization to extract/upload index with thousands or millions of documents.
In this case it's advisable to use a different tool to export/import data.

Currently the tool support:

- Index to import/export
- AWS IAM authentication with static credentials or dynamic credentials with STS, Roles or environment variables

Running
-------

The package install 2 cli applicantions:

- ``es-export`` (export the index to file)
    parameters

    Usage: es-export [OPTIONS]

      Elasticsearch Export program :return:

    Options:
      -i, --index <index>      Index name to export. Default: .kibana-4
      -f, --file <file>        JSON filename to export. Default: export.json
      -e, --es-host <host>     Elasticsearch host name or IP address.  [required]
      -p, --es-port <port>     Elasticsearch port number. Default is 80
      -t, --timeout <timeout>  Elasticsearch timeout connection. Default is 30
      -r, --region <region>    Change the region to run the program. Default is
                               us-east-1
      -vv, --verbose           Verbose output.
      -v, --version            Display version number and exit.
      --help                   Show this message and exit.

- ``es-import`` (import the index from file to elasticsearch)
    parameters

    Usage: es-import [OPTIONS]

      Elasticsearch Import program :return:

    Options:
      -i, --index <index>      Index name to export. Default: .kibana-4
      -f, --file <file>        JSON filename to import in the Elasticsearch.
                               Default: export.json  [required]
      -e, --es-host <host>     Elasticsearch host name or IP address.  [required]
      -p, --es-port <port>     Elasticsearch port number. Default is 80
      -t, --timeout <timeout>  Elasticsearch timeout connection. Default is 30
      -di, --delete-index      Delete current index before import. Default: false
      -r, --region <region>    Change the region to run the program. Default is
                               us-east-1
      -v, --version            Display version number and exit.
      --help                   Show this message and exit.

Changes
-------

- Version 0.1.4

    Bug fixes

- Version 0.1.3

    es_export wasn't getting the region parameter

- Version 0.1.2

    Corrected a problem where the kibana mapping was uploaded as document instead of mapping

- Version 0.1.0

    Initial version
