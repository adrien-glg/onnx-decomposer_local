#!/bin/bash

FUNCTION_NAME='mobiledet_slice0'
PACKAGE="mobiledet_slice0.zip"
PACKAGE_PATH="packages/mobiledet/slice0/${PACKAGE}"
S3_BUCKET="onnx-mobiledet-bucket"
LAMBDA_FUNCTION="mobiledet_lambda"

aws lambda delete-function --function-name mobiledet_slice0

aws s3 cp ${PACKAGE_PATH} s3://${S3_BUCKET}

aws lambda create-function --function-name ${FUNCTION_NAME} \
--code S3Bucket=${S3_BUCKET},S3Key=${PACKAGE} --handler mobiledet_lambda.lambda_handler --runtime python3.8 \
--role arn:aws:iam::426543810977:role/lambda-ex --timeout 30 --memory-size 256
