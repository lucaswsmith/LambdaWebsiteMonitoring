#!/usr/bin/env bash
cp websiteCheck.py lambda_function.py
chmod 755 lambda_function.py
zip lambda_function.zip lambda_function.py
aws s3 cp lambda_function.zip s3://lucas-smith-lambda-functions/websiteCheck/lambda_function.zip
rm lambda_function.py
rm lambda_function.zip
#  s3://lucas-smith-lambda-functions/websiteCheck/lambda_function.zip
aws cloudformation create-stack --stack-name znmdrTriggerMonitor --template-body file://cf_lambda.yaml --capabilities CAPABILITY_IAM 