#!/usr/bin/python
# -*- coding: utf-8 -*-
#####################################################################################################################
# Copyright 2019 Amazon.com, Inc. or its affiliates. All Rights Reserved.                                           #
#                                                                                                                   #
# Licensed under the Amazon Software License (the "License"). You may not use this file except in compliance        #
# with the License. A copy of the License is located at                                                             #
#                                                                                                                   #
#     http://aws.amazon.com/asl/                                                                                    #
#                                                                                                                   #
# or in the "license" file accompanying this file. This file is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES #
# OR CONDITIONS OF ANY KIND, express or implied. See the License for the specific language governing permissions    #
# and limitations under the License.                                                                                #
######################################################################################################################

import json
import logging
import uuid
from botocore.vendored import requests
from os import environ

logging.getLogger().debug('Loading function')

#======================================================================================================================
# Auxiliary Functions
#======================================================================================================================
def send_response(event, context, responseStatus, responseData, resourceId, reason=None):
    logging.getLogger().debug("[send_response] Start")

    responseUrl = event['ResponseURL']
    cw_logs_url = "https://console.aws.amazon.com/cloudwatch/home?region=%s#logEventViewer:group=%s;stream=%s"%(context.invoked_function_arn.split(':')[3], context.log_group_name, context.log_stream_name)

    logging.getLogger().info(responseUrl)
    responseBody = {}
    responseBody['Status'] = responseStatus
    responseBody['Reason'] = reason or ('See the details in CloudWatch Logs: ' +  cw_logs_url)
    responseBody['PhysicalResourceId'] = resourceId
    responseBody['StackId'] = event['StackId']
    responseBody['RequestId'] = event['RequestId']
    responseBody['LogicalResourceId'] = event['LogicalResourceId']
    responseBody['NoEcho'] = False
    responseBody['Data'] = responseData

    json_responseBody = json.dumps(responseBody)
    logging.getLogger().debug("Response body:\n" + json_responseBody)

    headers = {
        'content-type' : '',
        'content-length' : str(len(json_responseBody))
    }

    try:
        response = requests.put(responseUrl,
                                data=json_responseBody,
                                headers=headers)
        logging.getLogger().debug("Status code: " + response.reason)

    except Exception as error:
        logging.getLogger().error("[send_response] Failed executing requests.put(..)")
        logging.getLogger().error(str(error))

    logging.getLogger().debug("[send_response] End")

#======================================================================================================================
# Lambda Entry Point
#======================================================================================================================
def lambda_handler(event, context):
    responseStatus = 'SUCCESS'
    reason = None
    responseData = {}
    resourceId = event['PhysicalResourceId'] if 'PhysicalResourceId' in event else event['LogicalResourceId']
    result = {
        'StatusCode': '200',
        'Body':  {'message': 'success'}
    }

    try:
        #------------------------------------------------------------------
        # Set Log Level
        #------------------------------------------------------------------
        global log_level
        log_level = str(environ['LOG_LEVEL'].upper())
        if log_level not in ['DEBUG', 'INFO','WARNING', 'ERROR','CRITICAL']:
            log_level = 'ERROR'
        logging.getLogger().setLevel(log_level)

        #----------------------------------------------------------
        # Read inputs parameters
        #----------------------------------------------------------
        logging.getLogger().info(event)
        request_type = event['RequestType'].upper() if ('RequestType' in event) else ""
        logging.getLogger().info(request_type)

        #----------------------------------------------------------
        # Process event
        #----------------------------------------------------------
        if event['ResourceType'] == "Custom::CreateUUID":
            if 'CREATE' in request_type:
                responseData['UUID'] = str(uuid.uuid4())
                logging.getLogger().debug("UUID: %s"%responseData['UUID'])

            # UPDATE: do nothing
            # DELETE: do nothing

    except Exception as error:
        logging.getLogger().error(error)
        responseStatus = 'FAILED'
        reason = str(error)
        result = {
            'statusCode': '400',
            'body':  {'message': reason}
        }

    finally:
        #------------------------------------------------------------------
        # Send Result
        #------------------------------------------------------------------
        if 'ResponseURL' in event:
            send_response(event, context, responseStatus, responseData, resourceId, reason)

        return json.dumps(result)
