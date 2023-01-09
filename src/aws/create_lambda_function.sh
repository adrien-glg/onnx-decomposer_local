#!/bin/bash

source config.sh

aws lambda delete-function --function-name ${FUNCTION_NAME}

aws s3 cp ${ZIP_PACKAGE_PATH} s3://${S3_BUCKET}

aws lambda create-function --function-name ${FUNCTION_NAME} \
--code S3Bucket=${S3_BUCKET},S3Key=${ZIP_PACKAGE} --handler mobiledet_lambda.lambda_handler --runtime python3.8 \
--role arn:aws:iam::426543810977:role/lambda-ex --timeout 30 --memory-size 256
