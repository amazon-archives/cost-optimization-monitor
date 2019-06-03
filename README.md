# Cost Optimization Monitor
Source code for the AWS solution "Cost Optimization: Monitor".

For the full solution overview visit [Cost Optimization: Monitor](https://aws.amazon.com/answers/account-management/cost-optimization-monitor/).

## File Structure
```
|-deployment/ [folder containing templates and build scripts]
|-source/
  |-es-tools/ [this program is aimed to export and import kibana dashboards from/to Elastic Search clusters]
  |-helper/ [custom helper for CloudFormation deployment auxiliary functions]
```

## Getting Started

#### 01. Prerequisites
The following procedures assumes that all of the OS-level configuration has been completed. They are:

* [AWS Command Line Interface](https://aws.amazon.com/cli/)
* Python 3.x

The latest version has been tested with Python v3.7.

#### 02. Clone Cost Optimization Monitor repository
Clone the cost-optimization-monitor GitHub repository:

```
git clone https://github.com/awslabs/cost-optimization-monitor.git
```

#### 03. Declare enviroment variables:
```
export AWS_REGION=<aws-region-code>
export VERSION_CODE=<version-code>
export DEPLOY_BUCKET=<source-bucket-base-name>
```
- **aws-region-code**: AWS region code. Ex: ```us-east-1```.
- **version-code**: version of the package. EX: ```v1.1.0```.
- **source-bucket-base-name**: Name for the S3 bucket location where the template will source the Lambda code from. The template will append ```-[aws-region-code]``` to this bucket name. For example: ```./build-s3-dist.sh solutions v1.1.0```, the template will then expect the source code to be located in the ```solutions-[aws-region-code]``` bucket.

#### 04. Build the Cost Optimization Monitor solution for deployment:
```
cd ./cost-optimization-monitor/deployment
chmod +x build-s3-dist.sh
./build-s3-dist.sh $DEPLOY_BUCKET $VERSION_CODE
```
#### 05. Upload deployment assets to your Amazon S3 bucket:
```
aws s3 cp ./dist s3://$DEPLOY_BUCKET-$AWS_REGION/cost-optimization-monitor/latest --recursive --acl bucket-owner-full-control
aws s3 cp ./dist s3://$DEPLOY_BUCKET-$AWS_REGION/cost-optimization-monitor/$VERSION_CODE --recursive --acl bucket-owner-full-control
```

#### 06. Deploy the Cost Optimization Monitor solution:
* From your designated Amazon S3 bucket where you uploaded the deployment assets, copy the link location for the cost-optimization-monitor.template.
* Using AWS CloudFormation, launch the Cost Optimization Monitor solution stack using the copied Amazon S3 link for the cost-optimization-monitor.template.

***

Copyright 2019 Amazon.com, Inc. or its affiliates. All Rights Reserved.

Licensed under the Amazon Software License (the "License"). You may not use this file except in compliance with the License. A copy of the License is located at

    http://aws.amazon.com/asl/

or in the "license" file accompanying this file. This file is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, express or implied. See the License for the specific language governing permissions and limitations under the License.
