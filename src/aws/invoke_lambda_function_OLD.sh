#!/bin/bash

source config.sh

PAYLOAD="file://event0.json"
OUTPUT_EVENT="event1.json"

#aws lambda invoke --function-name mobiledet_slice0 --cli-binary-format raw-in-base64-out --payload file://event0.json event1.json
aws lambda invoke --function-name ${FUNCTION_NAME} --cli-binary-format raw-in-base64-out --payload ${PAYLOAD} ${OUTPUT_EVENT}

#cat lambda_output.json | jq .
cat ${OUTPUT_EVENT} | jq .
