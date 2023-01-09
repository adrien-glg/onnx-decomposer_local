#!/bin/bash

source config.sh

if [[ $# -eq 0 ]]
then
    echo "script usage: $0 [-l layer_number]"
    exit 1
fi


while getopts :l: flag
do
    case "${flag}" in
        l)
          layer_number=${OPTARG}
          ;;
    esac
done

INPUT_PAYLOAD="file://event${layer_number}.json"
OUTPUT_PAYLOAD_FULL="event$((${layer_number}+1))_full.json"
OUTPUT_PAYLOAD="event$((${layer_number}+1)).json"

aws lambda invoke --function-name ${FUNCTION_NAME} --cli-binary-format raw-in-base64-out --payload ${INPUT_PAYLOAD} ${OUTPUT_PAYLOAD_FULL}

cat ${OUTPUT_PAYLOAD_FULL} | jq .
cat ${OUTPUT_PAYLOAD_FULL} | jq .body > ${OUTPUT_PAYLOAD}


