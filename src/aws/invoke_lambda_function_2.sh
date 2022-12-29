#!/bin/bash

INPUT_EVENT=event1.json
OUTPUT_EVENT=event2.json

cat ${INPUT_EVENT} | jq .body > event1_body.json

#aws lambda invoke --function-name mobiledet_slice0 --cli-binary-format raw-in-base64-out --payload file://event0.json event1.json
aws lambda invoke --function-name mobiledet_slice0 --cli-binary-format raw-in-base64-out --payload file://event1_body.json ${OUTPUT_EVENT}

#cat lambda_output.json | jq .
cat ${OUTPUT_EVENT} | jq .
